"""
TensorFlow Lite Model Converter
"""

import tensorflow as tf
from pathlib import Path

def convert_to_tflite(
    model_path: str = 'trained_model.keras',
    output_path: str = 'models/plant_disease_model.tflite',
    quantize: bool = True
):
    """
    Convert model to TensorFlow Lite for mobile/edge deployment
    """
    # Load model
    model = tf.keras.models.load_model(model_path)
    
    # Convert to TFLite
    converter = tf.lite.TFLiteConverter.from_keras_model(model)
    
    if quantize:
        # Apply quantization for smaller model size
        converter.optimizations = [tf.lite.Optimize.DEFAULT]
    
    tflite_model = converter.convert()
    
    # Save model
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, 'wb') as f:
        f.write(tflite_model)
    
    print(f"TFLite model saved to {output_path}")
    print(f"Model size: {len(tflite_model) / 1024:.2f} KB")
    
    return output_path