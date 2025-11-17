from flask import Blueprint, request, jsonify
import io
from PIL import Image
from config import ALLOWED_EXTENSIONS

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
    from app.routes.main import get_detector
    detector = get_detector()

    for file in files:
        if file.filename == '':
            results.append({"error": "No file selected"})
            continue

        if file and allowed_file(file.filename):
            try:
                # Read image into memory
                img_data = file.read()
                img = Image.open(io.BytesIO(img_data))
                
                # Convert to RGB if needed
                if img.mode != 'RGB':
                    img = img.convert('RGB')
                
                # Create in-memory file-like object
                in_memory_file = io.BytesIO()
                img.save(in_memory_file, format='JPEG')
                in_memory_file.seek(0)
                
                # Process with detector
                if detector is None:
                    result = {"error": "Model not available"}
                else:
                    result = detector.predict_from_stream(in_memory_file)
                
                results.append(result)
            except Exception as e:
                results.append({"error": str(e)})
        else:
            results.append({"error": "Invalid file type", "filename": file.filename})

    return jsonify({"results": results})

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS