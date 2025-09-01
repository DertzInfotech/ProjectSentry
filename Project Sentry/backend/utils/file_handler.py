import os
import uuid
from werkzeug.utils import secure_filename

class FileHandler:
    def __init__(self, upload_folder):
        self.upload_folder = upload_folder
        self.allowed_extensions = {'ifc', 'IFC'}

    def allowed_file(self, filename):
        """Check if file has an allowed extension"""
        return '.' in filename and \
               filename.rsplit('.', 1)[1] in self.allowed_extensions

    def save_file(self, file, filename):
        """Save uploaded file with unique name"""
        # Generate unique filename to avoid conflicts
        name, ext = os.path.splitext(filename)
        unique_filename = f"{name}_{uuid.uuid4().hex[:8]}{ext}"

        file_path = os.path.join(self.upload_folder, unique_filename)
        file.save(file_path)

        return file_path

    def delete_file(self, file_path):
        """Delete file if it exists"""
        try:
            if os.path.exists(file_path):
                os.remove(file_path)
                return True
            return False
        except Exception as e:
            print(f"Error deleting file {file_path}: {str(e)}")
            return False

    def get_file_info(self, file_path):
        """Get file information"""
        if not os.path.exists(file_path):
            return None

        stat = os.stat(file_path)
        return {
            'size': stat.st_size,
            'created': stat.st_ctime,
            'modified': stat.st_mtime,
            'filename': os.path.basename(file_path)
        }
