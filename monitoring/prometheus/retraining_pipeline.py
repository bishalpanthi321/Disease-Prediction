"""
Automated Retraining Pipeline with Validation
"""

import numpy as np
from datetime import datetime
import logging
from typing import Dict

logger = logging.getLogger(__name__)


class RetrainingPipeline:
    """
    Automated retraining pipeline with validation
    """
    
    def __init__(self, model_path: str, data_dir: str):
        self.model_path = model_path
        self.data_dir = data_dir
        self.retraining_history = []
    
    def trigger_retraining(self, new_data: Dict, validation_data: Dict) -> Dict:
        """
        Trigger model retraining with new data
        """
        logger.info("Starting model retraining...")
        
        try:
            import tensorflow as tf
            
            # Load current model
            model = tf.keras.models.load_model(self.model_path)
            
            # Prepare training data
            X_new = np.array(new_data['images'])
            y_new = tf.keras.utils.to_categorical(new_data['labels'], num_classes=38)
            
            # Prepare validation data
            X_val = np.array(validation_data['images'])
            y_val = tf.keras.utils.to_categorical(validation_data['labels'], num_classes=38)
            
            # Create data augmentation
            data_augmentation = tf.keras.Sequential([
                tf.keras.layers.RandomFlip("horizontal"),
                tf.keras.layers.RandomRotation(0.2),
                tf.keras.layers.RandomZoom(0.2),
            ])
            
            # Apply augmentation
            X_new_augmented = data_augmentation(X_new, training=True)
            
            # Fine-tune with lower learning rate
            model.compile(
                optimizer=tf.keras.optimizers.Adam(learning_rate=0.00001),
                loss='categorical_crossentropy',
                metrics=['accuracy']
            )
            
            # Train
            history = model.fit(
                X_new_augmented, y_new,
                validation_data=(X_val, y_val),
                epochs=10,
                batch_size=32,
                verbose=1
            )
            
            # Evaluate
            val_loss, val_accuracy = model.evaluate(X_val, y_val, verbose=0)
            
            # Save new model with version
            new_version = len(self.retraining_history) + 1
            new_model_path = f"{self.model_path}.v{new_version}"
            model.save(new_model_path)
            
            retraining_record = {
                'version': new_version,
                'timestamp': datetime.utcnow().isoformat(),
                'training_samples': len(X_new),
                'validation_accuracy': float(val_accuracy),
                'validation_loss': float(val_loss),
                'model_path': new_model_path,
                'training_history': {
                    'accuracy': [float(x) for x in history.history['accuracy']],
                    'val_accuracy': [float(x) for x in history.history['val_accuracy']],
                    'loss': [float(x) for x in history.history['loss']],
                    'val_loss': [float(x) for x in history.history['val_loss']]
                }
            }
            
            self.retraining_history.append(retraining_record)
            
            logger.info(f"Retraining complete. Val Accuracy: {val_accuracy:.4f}")
            
            return retraining_record
        
        except Exception as e:
            logger.error(f"Retraining failed: {e}")
            return {'error': str(e)}
    
    def compare_models(self, old_model_path: str, new_model_path: str, 
                      test_data: Dict) -> Dict:
        """Compare old and new model performance"""
        import tensorflow as tf
        
        old_model = tf.keras.models.load_model(old_model_path)
        new_model = tf.keras.models.load_model(new_model_path)
        
        X_test = np.array(test_data['images'])
        y_test = tf.keras.utils.to_categorical(test_data['labels'], num_classes=38)
        
        old_loss, old_acc = old_model.evaluate(X_test, y_test, verbose=0)
        new_loss, new_acc = new_model.evaluate(X_test, y_test, verbose=0)
        
        improvement = new_acc - old_acc
        
        return {
            'old_model': {
                'accuracy': float(old_acc),
                'loss': float(old_loss)
            },
            'new_model': {
                'accuracy': float(new_acc),
                'loss': float(new_loss)
            },
            'improvement': float(improvement),
            'recommendation': 'DEPLOY' if improvement > 0.01 else 'ROLLBACK'
        }