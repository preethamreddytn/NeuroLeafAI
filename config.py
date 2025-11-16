import os

# Base directory
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

# Upload folder
UPLOAD_FOLDER = os.path.join(BASE_DIR, 'app', 'static', 'uploads')
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

# Model paths
MODEL_PATH = os.path.join(BASE_DIR, 'models', 'mobilenetv2_mixup_cutmix_best.keras')

# Create directories if they don't exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(os.path.join(BASE_DIR, 'models'), exist_ok=True)
os.makedirs(os.path.join(BASE_DIR, 'data'), exist_ok=True)