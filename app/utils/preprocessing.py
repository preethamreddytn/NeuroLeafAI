import cv2
import numpy as np
from PIL import Image

def preprocess_image(image_path, target_size=(224, 224)):
    """
    Preprocess an image for model prediction
    
    Args:
        image_path (str): Path to the image file
        target_size (tuple): Target size for the image (width, height)
    
    Returns:
        numpy.ndarray: Preprocessed image array
    """
    # Read the image
    image = cv2.imread(image_path)
    
    # Convert BGR to RGB
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    
    # Resize the image
    image = cv2.resize(image, target_size)
    
    # Normalize pixel values to [0, 1]
    image = image.astype(np.float32) / 255.0
    
    # Expand dimensions to match model input shape
    image = np.expand_dims(image, axis=0)
    
    return image

def augment_image(image):
    """
    Apply basic augmentation to an image
    
    Args:
        image (numpy.ndarray): Input image array
    
    Returns:
        numpy.ndarray: Augmented image array
    """
    # Random horizontal flip
    if np.random.random() > 0.5:
        image = np.fliplr(image)
    
    # Random rotation (up to 15 degrees)
    angle = np.random.uniform(-15, 15)
    # Note: Actual rotation implementation would require additional libraries
    
    return image

def resize_image(image_path, max_size=(800, 600)):
    """
    Resize an image to a maximum size while maintaining aspect ratio
    
    Args:
        image_path (str): Path to the image file
        max_size (tuple): Maximum size (width, height)
    
    Returns:
        PIL.Image: Resized image
    """
    image = Image.open(image_path)
    
    # Calculate new size maintaining aspect ratio
    image.thumbnail(max_size, Image.LANCZOS)
    
    return image