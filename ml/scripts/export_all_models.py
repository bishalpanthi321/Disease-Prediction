"""
Export All Model Formats
Main script to run all exports
"""

import sys
from pathlib import Path

# Add parent directory to path
sys.path.append(str(Path(__file__).parent.parent.parent))

from ml.export.serving_exporter import export_model_for_serving
from ml.export.tflite_converter import convert_to_tflite
from ml.export.onnx_converter import convert_to_onnx
from ml.export.docker_config import create_docker_compose


if __name__ == "__main__":
    # Export model for TensorFlow Serving
    print("Exporting model for TensorFlow Serving...")
    export_model_for_serving()
    
    # Convert to TFLite for mobile
    print("\nConverting model to TFLite...")
    convert_to_tflite()
    
    # Convert to ONNX
    print("\nConverting model to ONNX...")
    convert_to_onnx()
    
    # Create Docker Compose
    print("\nCreating Docker Compose configuration...")
    create_docker_compose()
    
    print("\n=== Model Export Complete ===")
    print("To start TensorFlow Serving:")
    print("  docker-compose -f docker-compose.serving.yml up")