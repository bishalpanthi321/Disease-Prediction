"""
ONNX Model Converter
"""

import tensorflow as tf
from pathlib import Path

def convert_to_onnx(
    model_path: str = 'trained_model.keras',
    output_path: str = 'models/plant_disease_model.onnx'
):
    """
    Convert model to ONNX format for cross-platform deployment
    Requires: tf2onnx library
    """
    try:
        import tf2onnx
        import onnx
        
        # Load model
        model = tf.keras.models.load_model(model_path)
        
        # Convert to ONNX
        spec = (tf.TensorSpec((None, 128, 128, 3), tf.float32, name="input"),)
        output_path_full = output_path
        
        model_proto, _ = tf2onnx.convert.from_keras(
            model,
            input_signature=spec,
            opset=13,
            output_path=output_path_full
        )
        
        print(f"ONNX model saved to {output_path_full}")
        
        # Verify ONNX model
        onnx_model = onnx.load(output_path_full)
        onnx.checker.check_model(onnx_model)
        print("ONNX model verified successfully")
        
        return output_path_full
    
    except ImportError:
        print("tf2onnx not installed. Install with: pip install tf2onnx onnx")
        return None