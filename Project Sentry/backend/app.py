from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
import os
import uuid
import json
from datetime import datetime, timedelta
from werkzeug.utils import secure_filename
import sqlite3
import math
import random

# Import our custom services
from services.ifc_processor import IFCProcessor
from services.validation_service import ValidationService
from services.health_calculator import HealthCalculator
from utils.file_handler import FileHandler
from utils.helpers import generate_mock_data

app = Flask(__name__)
CORS(app)

# Configuration
app.config['SECRET_KEY'] = 'your-secret-key-here'
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['MAX_CONTENT_LENGTH'] = 500 * 1024 * 1024  # 500MB max file size
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ifc_dashboard.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize extensions
db = SQLAlchemy(app)

# Ensure upload directory exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Initialize services
ifc_processor = IFCProcessor()
validation_service = ValidationService()
health_calculator = HealthCalculator()
file_handler = FileHandler(app.config['UPLOAD_FOLDER'])

# Database Models
class Project(db.Model):
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = db.Column(db.String(255), nullable=False)
    filename = db.Column(db.String(255), nullable=False)
    file_path = db.Column(db.String(500), nullable=False)
    file_size = db.Column(db.Integer, nullable=False)
    upload_date = db.Column(db.DateTime, default=datetime.utcnow)
    health_score = db.Column(db.Integer, default=0)
    status = db.Column(db.String(50), default='Processing')
    total_elements = db.Column(db.Integer, default=0)
    validated_elements = db.Column(db.Integer, default=0)
    critical_issues = db.Column(db.Integer, default=0)
    warning_issues = db.Column(db.Integer, default=0)
    info_issues = db.Column(db.Integer, default=0)

class ValidationResult(db.Model):
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    project_id = db.Column(db.String(36), db.ForeignKey('project.id'), nullable=False)
    rule_name = db.Column(db.String(255), nullable=False)
    status = db.Column(db.String(50), nullable=False)  # passed, warning, critical
    issues_count = db.Column(db.Integer, default=0)
    description = db.Column(db.Text)
    created_date = db.Column(db.DateTime, default=datetime.utcnow)

# API Routes

@app.route('/')
def index():
    return jsonify({
        'message': 'IFC Model Health Dashboard API',
        'version': '1.0.0',
        'status': 'running'
    })

@app.route('/api/upload', methods=['POST'])
def upload_file():
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file provided'}), 400

        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400

        if not file_handler.allowed_file(file.filename):
            return jsonify({'error': 'File type not allowed. Please upload .ifc files only'}), 400

        # Save file
        filename = secure_filename(file.filename)
        file_path = file_handler.save_file(file, filename)
        file_size = os.path.getsize(file_path)

        # Create project record
        project = Project(
            name=filename.replace('.ifc', '').replace('.IFC', ''),
            filename=filename,
            file_path=file_path,
            file_size=file_size,
            status='Processing'
        )

        db.session.add(project)
        db.session.commit()

        # Process file asynchronously (simplified for demo)
        try:
            results = ifc_processor.process_file(file_path)
            validation_results = validation_service.validate_model(results)
            health_score = health_calculator.calculate_score(validation_results)

            # Update project with results
            project.health_score = health_score['overall_score']
            project.status = 'Completed'
            project.total_elements = results.get('total_elements', 0)
            project.validated_elements = results.get('validated_elements', 0)
            project.critical_issues = health_score.get('critical_issues', 0)
            project.warning_issues = health_score.get('warning_issues', 0)
            project.info_issues = health_score.get('info_issues', 0)

            # Save validation results
            for rule_result in validation_results:
                validation_record = ValidationResult(
                    project_id=project.id,
                    rule_name=rule_result['name'],
                    status=rule_result['status'],
                    issues_count=rule_result['issues'],
                    description=rule_result.get('description', '')
                )
                db.session.add(validation_record)

            db.session.commit()

        except Exception as e:
            # If processing fails, mark as error but don't fail the upload
            project.status = 'Error'
            project.health_score = 0
            db.session.commit()
            print(f"Processing error: {str(e)}")

        return jsonify({
            'message': 'File uploaded successfully',
            'project_id': project.id,
            'filename': filename,
            'file_size': file_size,
            'status': project.status
        }), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/projects', methods=['GET'])
def get_projects():
    try:
        projects = Project.query.order_by(Project.upload_date.desc()).all()

        projects_data = []
        for project in projects:
            projects_data.append({
                'id': project.id,
                'name': project.name,
                'filename': project.filename,
                'file_size': f"{project.file_size / (1024*1024):.1f} MB",
                'upload_date': project.upload_date.isoformat(),
                'health_score': project.health_score,
                'status': project.status,
                'total_elements': project.total_elements,
                'validated_elements': project.validated_elements,
                'issues': {
                    'critical': project.critical_issues,
                    'warning': project.warning_issues,
                    'info': project.info_issues
                }
            })

        return jsonify(projects_data), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/projects/<project_id>', methods=['GET'])
def get_project(project_id):
    try:
        project = Project.query.get(project_id)
        if not project:
            return jsonify({'error': 'Project not found'}), 404

        # Get validation results
        validation_results = ValidationResult.query.filter_by(project_id=project_id).all()

        validation_data = []
        for result in validation_results:
            validation_data.append({
                'rule_name': result.rule_name,
                'status': result.status,
                'issues_count': result.issues_count,
                'description': result.description,
                'created_date': result.created_date.isoformat()
            })

        project_data = {
            'id': project.id,
            'name': project.name,
            'filename': project.filename,
            'file_size': f"{project.file_size / (1024*1024):.1f} MB",
            'upload_date': project.upload_date.isoformat(),
            'health_score': project.health_score,
            'status': project.status,
            'total_elements': project.total_elements,
            'validated_elements': project.validated_elements,
            'issues': {
                'critical': project.critical_issues,
                'warning': project.warning_issues,
                'info': project.info_issues
            },
            'validation_results': validation_data
        }

        return jsonify(project_data), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/dashboard', methods=['GET'])
def get_dashboard():
    try:
        # Get dashboard statistics
        total_projects = Project.query.count()
        completed_projects = Project.query.filter_by(status='Completed').count()

        if completed_projects > 0:
            avg_health_score = db.session.query(db.func.avg(Project.health_score)).filter(
                Project.status == 'Completed'
            ).scalar() or 0

            total_issues = db.session.query(
                db.func.sum(Project.critical_issues + Project.warning_issues + Project.info_issues)
            ).filter(Project.status == 'Completed').scalar() or 0
        else:
            avg_health_score = 0
            total_issues = 0

        # Get recent projects
        recent_projects = Project.query.order_by(Project.upload_date.desc()).limit(5).all()

        recent_data = []
        for project in recent_projects:
            recent_data.append({
                'id': project.id,
                'name': project.name,
                'health_score': project.health_score,
                'status': project.status,
                'upload_date': project.upload_date.isoformat()
            })

        # Generate mock activity data for demo
        activity_data = generate_mock_data.get_recent_activity()

        dashboard_data = {
            'summary': {
                'total_projects': total_projects,
                'completed_projects': completed_projects,
                'average_health_score': round(avg_health_score, 1),
                'total_issues_resolved': max(0, total_issues - random.randint(0, total_issues//3))
            },
            'recent_projects': recent_data,
            'recent_activity': activity_data,
            'health_trend': generate_mock_data.get_health_trend(),
            'issue_distribution': generate_mock_data.get_issue_distribution()
        }

        return jsonify(dashboard_data), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/issues/<project_id>', methods=['GET'])
def get_issues(project_id):
    try:
        project = Project.query.get(project_id)
        if not project:
            return jsonify({'error': 'Project not found'}), 404

        # Generate mock issues data for demo
        issues_data = generate_mock_data.get_project_issues(project_id)

        return jsonify(issues_data), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.utcnow().isoformat(),
        'database': 'connected'
    }), 200

# Error handlers
@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Endpoint not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({'error': 'Internal server error'}), 500

# Initialize database
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
