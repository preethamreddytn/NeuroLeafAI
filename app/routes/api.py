from flask import Blueprint, request, jsonify
import os
from werkzeug.utils import secure_filename
from config import ALLOWED_EXTENSIONS, UPLOAD_FOLDER

api_bp = Blueprint('api', __name__)

@api_bp.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({"status": "healthy", "service": "BioAgriCure API"})

@api_bp.route('/api/detect', methods=['POST'])
def detect_disease():
    """API endpoint for disease detection"""
    # Support multiple files in 'files' or single 'file' for backwards compatibility
    files = []
    if 'files' in request.files:
        files = request.files.getlist('files')
    elif 'file' in request.files:
        files = [request.files['file']]

    if not files:
        return jsonify({"error": "No file provided"}), 400

    results = []
    import time

    for file in files:
        if file.filename == '':
            results.append({"error": "No file selected"})
            continue

        if file and allowed_file(file.filename):
            safe_name = secure_filename(file.filename or f'upload-{int(time.time())}.jpg')
            filename = f"{int(time.time()*1000)}_{safe_name}"
            filepath = os.path.join(UPLOAD_FOLDER, filename)
            file.save(filepath)

            # TODO: plug in model prediction here
            # For now return placeholder per-file
            results.append({"filename": filename, "status": "received", "message": "Model not implemented"})
        else:
            results.append({"error": "Invalid file type", "filename": file.filename})

    return jsonify({"results": results})

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS