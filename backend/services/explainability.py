"""
Explainability Service - Grad-CAM implementation
"""
import tensorflow as tf
import numpy as np
import logging

logger = logging.getLogger(__name__)

def generate_explainability_map(image: np.ndarray, model, predicted_class_idx: int):
    """Generate Grad-CAM heatmap for explainability"""
    try:
        # Get last conv layer
        last_conv_layer = None
        for layer in reversed(model.layers):
            if isinstance(layer, tf.keras.layers.Conv2D):
                last_conv_layer = layer
                break
        
        if last_conv_layer is None:
            return None
        
        grad_model = tf.keras.models.Model(
            [model.inputs],
            [last_conv_layer.output, model.output]
        )
        
        with tf.GradientTape() as tape:
            conv_outputs, predictions = grad_model(image)
            loss = predictions[:, predicted_class_idx]
        
        grads = tape.gradient(loss, conv_outputs)
        pooled_grads = tf.reduce_mean(grads, axis=(0, 1, 2))
        
        conv_outputs = conv_outputs[0]
        heatmap = tf.reduce_sum(tf.multiply(pooled_grads, conv_outputs), axis=-1)
        heatmap = tf.maximum(heatmap, 0) / tf.math.reduce_max(heatmap)
        
        return heatmap.numpy().tolist()
    except Exception as e:
        logger.error(f"Error generating explainability map: {e}")
        return None