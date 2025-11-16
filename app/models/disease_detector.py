import os
import numpy as np
import pandas as pd
from tensorflow.keras.preprocessing import image
from tensorflow.keras.models import load_model
from config import MODEL_PATH

class DiseaseDetector:
    def __init__(self):
        """
        Initialize the disease detector with the trained MobileNetV2 model
        """
        self.model = None
        self.class_names = CLASS_LABELS = {
    0:  "American Bollworm on Cotton",
    1:  "Anthracnose on Cotton",
    2:  "Army Worm",
    3:  "Bacterial Blight in Rice",
    4:  "Brown Spot",
    5:  "Common Rust",
    6:  "Cotton Aphid",
    7:  "Flag Smut",
    8:  "Gray Leaf Spot",
    9:  "Healthy Maize",
    10: "Healthy Wheat",
    11: "Healthy Cotton",
    12: "Leaf Curl",
    13: "Leaf Smut",
    14: "Mosaic (sugarcane)",
    15: "RedRot (sugarcane)",
    16: "RedRust (sugarcane)",
    17: "Rice Blast",
    18: "Sugarcane Healthy",
    19: "Tungro",
    20: "Wheat Brown Leaf Rust",
    21: "Wheat Stem Fly",
    22: "Wheat Aphid",
    23: "Wheat Black Rust",
    24: "Bollworm on Cotton",
    25: "Wheat Mite",
    26: "Wheat Powdery Mildew",
    27: "Wheat Scab",
    28: "Wheat Yellow Rust",
    29: "Wilt",
    30: "Yellow Rust (Sugarcane)",
    31: "Bacterial Blight in Cotton",
    32: "Bollrot on Cotton",
    33: "Wheat Leaf Blight",
    34: "Cotton Mealy Bug",
    35: "Cotton Whitefly",
    36: "Maize Ear Rot",
    37: "Maize Fall Armyworm",
    38: "Maize Stem borer",
    39: "Pink Bollworm in Cotton",
    40: "Red Cotton Bug",
    41: "Thrips on Cotton",
}
        self.load_model()
        self.load_disease_info_csv()
    
    def load_disease_info_csv(self):
        """
        Load disease information from CSV file
        """
        csv_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'routes', 'disease_info.csv')
        try:
            if os.path.exists(csv_path):
                self.disease_info_df = pd.read_csv(csv_path)
                print(f"✓ Disease info CSV loaded: {len(self.disease_info_df)} diseases")
            else:
                print(f"⚠ Disease info CSV not found at: {csv_path}")
                self.disease_info_df = None
        except Exception as e:
            print(f"✗ Error loading disease info CSV: {e}")
            self.disease_info_df = None
    
    def load_model(self):
        """
        Load the trained MobileNetV2 model from file
        """
        if os.path.exists(MODEL_PATH):
            try:
                self.model = load_model(MODEL_PATH)
                print(f"✓ Model loaded successfully from {MODEL_PATH}")
                print(f"  - Input shape: {self.model.input_shape}")
                print(f"  - Output classes: {self.model.output_shape[-1]}")
            except Exception as e:
                print(f"✗ Error loading model: {e}")
                self.model = None
        else:
            print(f"✗ Model not found at {MODEL_PATH}")
            print("  Please ensure the model file exists or train a new model.")
    
    def preprocess_image(self, img_path):
        """
        Preprocess the image for MobileNetV2 prediction
        - Resize to 224x224
        - Normalize to [0, 1] range
        """
        img = image.load_img(img_path, target_size=(224, 224))
        img_array = image.img_to_array(img)
        img_array = np.expand_dims(img_array, axis=0)
        img_array = img_array / 255.0 
        return img_array
    
    def predict(self, img_path):
        """
        Predict the disease from an image
        """
        if self.model is None:
            return {
                "disease": "Model Not Available",
                "confidence": 0.0,
                "symptoms": ["The disease detection model is not loaded. Please train the model first."],
                "cure": ["Train the model by running: python train.py"]
            }
        
        img_array = self.preprocess_image(img_path)
        
        predictions = self.model.predict(img_array)
        predicted_class = np.argmax(predictions[0])
        confidence = np.max(predictions[0])
        
        if confidence < 0.5:  
            return {
                "disease": "Unable to Detect Disease",
                "confidence": float(confidence),
                "symptoms": ["The model is not confident about this image", "Please upload a clearer image of the affected plant"],
                "cure": ["Ensure good lighting and focus", "Take a close-up photo of the diseased area", "Consult a local agricultural expert if needed"]
            }
        
        disease_name = self.class_names[predicted_class] if predicted_class < len(self.class_names) else "Unknown Disease"
        
        formatted_name = self._format_disease_name(disease_name)
        disease_info = self.get_disease_info(disease_name)
        
        return {
            "disease": formatted_name,
            "confidence": float(confidence),
            "symptoms": disease_info["symptoms"],
            "cure": disease_info["cure"]
        }
    
    def _format_disease_name(self, raw_name):
        """
        Format disease name from model output to human-readable format
        Example: "Apple___Apple_scab" -> "Apple - Apple Scab"
        """
        if "___" in raw_name:
            parts = raw_name.split("___")
            plant = parts[0].replace("_", " ")
            disease = parts[1].replace("_", " ").title()
            return f"{plant} - {disease}"
        else:
            return raw_name.replace("_", " ").title()
    
    def get_disease_info(self, disease_name):
        """
        Get symptoms and cure information for a disease from CSV file
        Returns actual info if available, otherwise returns "information not available" message
        """
        if self.disease_info_df is not None:
            try:
                disease_row = self.disease_info_df[self.disease_info_df['disease_name'].str.lower() == disease_name.lower()]
                
                if not disease_row.empty:
                    row = disease_row.iloc[0]
                    symptoms = []
                    cures = []
                    
                    for col in ['symptom_1', 'symptom_2', 'symptom_3']:
                        if col in row and pd.notna(row[col]) and str(row[col]).strip():
                            symptoms.append(str(row[col]))
                    
                    for col in ['cure_1', 'cure_2']:
                        if col in row and pd.notna(row[col]) and str(row[col]).strip():
                            cures.append(str(row[col]))
                    
                    if symptoms and cures:
                        return {
                            "symptoms": symptoms,
                            "cure": cures
                        }
            except Exception as e:
                print(f"Error reading CSV for {disease_name}: {e}")
        
        return {
            "symptoms": ["Symptoms and cure information not available."],
            "cure": ["Please consult an agricultural expert for accurate diagnosis and treatment."]
        }