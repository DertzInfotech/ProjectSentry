import random
import uuid
from datetime import datetime, timedelta

class MockDataGenerator:
    def __init__(self):
        self.users = [
            'John Smith', 'Sarah Johnson', 'Mike Chen', 'Emma Wilson',
            'David Rodriguez', 'Lisa Anderson', 'Tom Brown', 'Anna Martinez'
        ]

        self.actions = [
            'Resolved clash issue', 'Uploaded new model version', 'Added property set validation rule',
            'Fixed geometry error', 'Updated material properties', 'Completed model review',
            'Assigned issue to team member', 'Approved model validation', 'Created custom rule',
            'Generated compliance report'
        ]

        self.issue_types = [
            {
                'type': 'Missing Properties',
                'severity': 'warning',
                'description': 'Elements missing required property sets'
            },
            {
                'type': 'Geometry Clashes',
                'severity': 'critical',
                'description': 'Physical interferences detected'
            },
            {
                'type': 'Naming Convention',
                'severity': 'info',
                'description': 'Non-standard naming detected'
            },
            {
                'type': 'Material Data',
                'severity': 'warning',
                'description': 'Incomplete material information'
            },
            {
                'type': 'Schema Validation',
                'severity': 'critical',
                'description': 'IFC schema compliance issues'
            },
            {
                'type': 'Unit Consistency',
                'severity': 'warning',
                'description': 'Inconsistent units detected'
            }
        ]

    def get_recent_activity(self, days=7, count=10):
        """Generate mock recent activity data"""
        activities = []

        for _ in range(count):
            timestamp = datetime.utcnow() - timedelta(
                days=random.uniform(0, days),
                hours=random.uniform(0, 24),
                minutes=random.uniform(0, 60)
            )

            activities.append({
                'id': str(uuid.uuid4()),
                'timestamp': timestamp.isoformat(),
                'user': random.choice(self.users),
                'action': random.choice(self.actions),
                'type': random.choice(['resolution', 'upload', 'configuration', 'review']),
                'project': f"Project {random.randint(1, 20)}"
            })

        # Sort by timestamp (most recent first)
        activities.sort(key=lambda x: x['timestamp'], reverse=True)
        return activities

    def get_health_trend(self, days=30):
        """Generate mock health trend data"""
        trend_data = []
        base_score = random.uniform(70, 85)

        for i in range(days):
            date = datetime.utcnow() - timedelta(days=days-i-1)

            # Add some realistic variation
            variation = random.uniform(-3, 5)
            base_score = max(0, min(100, base_score + variation))

            trend_data.append({
                'date': date.strftime('%Y-%m-%d'),
                'score': round(base_score, 1),
                'projects': random.randint(1, 5)
            })

        return trend_data

    def get_issue_distribution(self):
        """Generate mock issue distribution data"""
        total_issues = random.randint(50, 300)

        distribution = []
        remaining_issues = total_issues

        for issue_type in self.issue_types:
            if remaining_issues <= 0:
                count = 0
            else:
                max_count = min(remaining_issues, total_issues // 2)
                count = random.randint(0, max_count)
                remaining_issues -= count

            distribution.append({
                'type': issue_type['type'],
                'count': count,
                'severity': issue_type['severity'],
                'percentage': round((count / total_issues) * 100, 1) if total_issues > 0 else 0
            })

        return distribution

    def get_project_issues(self, project_id, count=None):
        """Generate mock issues for a specific project"""
        if count is None:
            count = random.randint(10, 50)

        issues = []

        for i in range(count):
            issue_type = random.choice(self.issue_types)

            issue = {
                'id': str(uuid.uuid4()),
                'project_id': project_id,
                'type': issue_type['type'],
                'severity': issue_type['severity'],
                'description': issue_type['description'],
                'element_id': f"Element_{random.randint(1000, 9999)}",
                'element_type': random.choice(['IfcWall', 'IfcSlab', 'IfcBeam', 'IfcColumn', 'IfcDoor', 'IfcWindow']),
                'status': random.choice(['Open', 'In Progress', 'Resolved', 'Closed']),
                'assigned_to': random.choice(self.users),
                'priority': random.choice(['Low', 'Medium', 'High', 'Critical']),
                'created_date': (datetime.utcnow() - timedelta(days=random.randint(1, 30))).isoformat(),
                'location': {
                    'story': f"Level {random.randint(1, 10)}",
                    'coordinates': {
                        'x': round(random.uniform(0, 100), 2),
                        'y': round(random.uniform(0, 100), 2),
                        'z': round(random.uniform(0, 30), 2)
                    }
                },
                'details': f"Detailed description of {issue_type['type'].lower()} issue found in the model.",
                'comments': [
                    {
                        'user': random.choice(self.users),
                        'timestamp': (datetime.utcnow() - timedelta(hours=random.randint(1, 48))).isoformat(),
                        'message': f"Initial assessment completed for this {issue_type['severity']} issue."
                    }
                ]
            }

            issues.append(issue)

        return issues

# Create global instance
generate_mock_data = MockDataGenerator()
