"""
Model Service - Handles model loading and predictions
"""
import tensorflow as tf
import numpy as np
from PIL import Image
import logging
from backend.config import CLASS_NAMES, MODEL_PATH, MODEL_VERSION
from backend.schemas.common import SeverityLevel

logger = logging.getLogger(__name__)

class ModelManager:
    def __init__(self):
        self.model = None
        self.model_version = MODEL_VERSION
        self.load_model()
        
    def load_model(self):
        """Load the TensorFlow model"""
        try:
            self.model = tf.keras.models.load_model(MODEL_PATH)
            logger.info(f"Model loaded successfully - Version {self.model_version}")
        except Exception as e:
            logger.error(f"Failed to load model: {e}")
            raise
    
    def preprocess_image(self, image: Image.Image) -> np.ndarray:
        """Preprocess image for prediction"""
        image = image.resize((128, 128))
        image_array = np.array(image) / 255.0
        return np.expand_dims(image_array, axis=0)
    
    def predict(self, image: Image.Image) -> tuple:
        """Make prediction and return class and confidence"""
        processed_image = self.preprocess_image(image)
        predictions = self.model.predict(processed_image)
        predicted_idx = np.argmax(predictions[0])
        confidence = float(predictions[0][predicted_idx])
        
        # Get all probabilities
        all_probs = {CLASS_NAMES[i]: float(predictions[0][i]) for i in range(len(CLASS_NAMES))}
        
        return CLASS_NAMES[predicted_idx], confidence, all_probs
    
    def estimate_severity(self, predicted_class: str, confidence: float, metadata: dict) -> str:
        """Estimate disease severity based on prediction and metadata"""
        if "healthy" in predicted_class.lower():
            return SeverityLevel.HEALTHY
        
        # Simple heuristic - can be replaced with ML model
        if confidence > 0.9:
            return SeverityLevel.SEVERE
        elif confidence > 0.75:
            return SeverityLevel.MODERATE
        elif confidence > 0.6:
            return SeverityLevel.MILD
        else:
            return SeverityLevel.HEALTHY

# Singleton instance
model_manager = ModelManager()

def get_model_manager() -> ModelManager:
    """Get model manager instance"""
    return model_manager