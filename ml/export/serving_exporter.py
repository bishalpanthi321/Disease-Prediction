"""
TensorFlow Serving Model Export and Configuration
Enables scalable model serving with versioning
"""

import tensorflow as tf
import os
import json
from pathlib import Path

def export_model_for_serving(
    model_path: str = 'trained_model.keras',
    export_dir: str = 'models/plant_disease',
    version: int = 1
):
    """
    Export trained model for TensorFlow Serving
    """
    # Load the model
    model = tf.keras.models.load_model(model_path)
    
    # Create export directory with version
    export_path = os.path.join(export_dir, str(version))
    Path(export_path).mkdir(parents=True, exist_ok=True)
    
    # Save model in SavedModel format
    tf.saved_model.save(model, export_path)
    
    print(f"Model exported to {export_path}")
    
    # Create model config for TensorFlow Serving
    model_config = {
        "model_config_list": [{
            "name": "plant_disease_model",
            "base_path": export_dir,
            "model_platform": "tensorflow",
            "model_version_policy": {
                "specific": {
                    "versions": [version]
                }
            }
        }]
    }
    
    config_path = os.path.join(export_dir, 'models.config')
    with open(config_path, 'w') as f:
        json.dump(model_config, f, indent=2)
    
    print(f"Model config saved to {config_path}")
    
    return export_path