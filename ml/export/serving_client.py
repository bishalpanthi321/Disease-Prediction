"""
TensorFlow Serving Client
"""

import requests
import numpy as np
from PIL import Image

def create_serving_client():
    """
    Example client for TensorFlow Serving
    """
    
    class TFServingClient:
        def __init__(self, server_url: str = "http://localhost:8501"):
            self.server_url = server_url
            self.model_name = "plant_disease_model"
        
        def predict(self, image_path: str):
            """Make prediction using TF Serving"""
            # Load and preprocess image
            image = Image.open(image_path).convert('RGB')
            image = image.resize((128, 128))
            image_array = np.array(image) / 255.0
            image_array = np.expand_dims(image_array, axis=0)
            
            # Prepare request
            url = f"{self.server_url}/v1/models/{self.model_name}:predict"
            data = {
                "instances": image_array.tolist()
            }
            
            # Send request
            response = requests.post(url, json=data)
            
            if response.status_code == 200:
                predictions = response.json()['predictions'][0]
                predicted_idx = np.argmax(predictions)
                confidence = predictions[predicted_idx]
                
                return {
                    "predicted_class": predicted_idx,
                    "confidence": confidence,
                    "all_predictions": predictions
                }
            else:
                raise Exception(f"Prediction failed: {response.text}")
    
    return TFServingClient