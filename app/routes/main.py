    from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
    import os
    import time
    from werkzeug.utils import secure_filename
    from config import ALLOWED_EXTENSIONS, UPLOAD_FOLDER
    from app.models.disease_detector import DiseaseDetector

    main_bp = Blueprint('main', __name__)


    detector = DiseaseDetector()

    @main_bp.route('/')
    def index():
        return render_template('index.html')

    @main_bp.route('/upload', methods=['GET', 'POST'])
    def upload():
        if request.method == 'POST':
            # Handle file upload (support multiple files)
            if 'files' not in request.files and 'file' not in request.files:
                flash('No file selected')
                return redirect(request.url)

            # Support both single 'file' (legacy) and multiple 'files'
            files = []
            if 'files' in request.files:
                files = request.files.getlist('files')
            elif 'file' in request.files:
                files = [request.files['file']]

            # Validate presence and check for empty filenames
            if not files or all(f.filename == '' for f in files):
                flash('No file selected. Please choose an image or take a photo.')
                return redirect(request.url)

            results = []
            for file in files:
                if file and allowed_file(file.filename):
                    # Create a unique filename to avoid collisions
                    safe_name = secure_filename(file.filename or f'upload-{int(time.time())}.jpg')
                    filename = f"{int(time.time()*1000)}_{safe_name}"
                    filepath = os.path.join(UPLOAD_FOLDER, filename)
                    file.save(filepath)

                    # Process the file with our CNN model
                    try:
                        res = detector.predict(filepath)
                    except Exception as e:
                        # On model errors, include an error entry but continue
                        res = {"error": str(e)}

                    res['image_filename'] = filename
                    results.append(res)

            # Render results page with all predictions
            return render_template('result.html', results=results)
        return render_template('upload.html')

    @main_bp.route('/result')
    def result():
        # Results are now passed directly from upload route
        return render_template('result.html', result=None)

    @main_bp.route('/about')
    def about():
        return render_template('about.html')

    @main_bp.route('/contact', methods=['GET', 'POST'])
    def contact():
        if request.method == 'POST':
            # Get form data
            name = request.form.get('name')
            email = request.form.get('email')
            message = request.form.get('message')
            
            # For now, just show success message
            # In production, you would send email or save to database
            flash('Thank you for contacting BioAgriCure! We\'ll get back to you soon.', 'success')
            return redirect(url_for('main.contact'))
        
        return render_template('contact.html')

    def allowed_file(filename):
        return (
            '.' in filename and
            filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
        )

