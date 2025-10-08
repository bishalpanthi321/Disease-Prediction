"""
ONNX Model Converter (Alternative using keras2onnx)
"""

import tensorflow as tf
from pathlib import Path

def convert_to_onnx(
    model_path: str = 'trained_model.keras',
    output_path: str = 'models/plant_disease_model.onnx'
):
    """
    Convert model to ONNX format for cross-platform deployment
    Requires: keras2onnx library
    """
    try:
        import keras2onnx
        import onnx
        
        # Load model
        model = tf.keras.models.load_model(model_path)
        
        # Convert to ONNX
        onnx_model = keras2onnx.convert_keras(
            model,
            name='plant_disease_model',
            target_opset=13
        )
        
        # Save ONNX model
        onnx.save_model(onnx_model, output_path)
        
        print(f"ONNX model saved to {output_path}")
        
        # Verify ONNX model
        onnx.checker.check_model(onnx_model)
        print("ONNX model verified successfully")
        
        return output_path
    
    except ImportError:
        print("keras2onnx not installed. Install with: conda install -c conda-forge keras2onnx onnx")
        return None