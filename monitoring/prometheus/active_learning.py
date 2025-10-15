"""
Active Learning Manager for Continuous Improvement
"""

import numpy as np
from datetime import datetime
import logging
from typing import Dict, List

logger = logging.getLogger(__name__)


class ActiveLearningManager:
    """
    Manages active learning pipeline for continuous improvement
    """
    
    def __init__(self, uncertainty_threshold: float = 0.7):
        self.uncertainty_threshold = uncertainty_threshold
        self.uncertain_samples = []
        self.labeled_pool = []
        
    def identify_uncertain_samples(self, predictions: np.ndarray, 
                                   images: List, metadata: List) -> List[Dict]:
        """
        Identify samples where model is uncertain for human review
        Uses multiple uncertainty measures
        """
        uncertain_samples = []
        
        for i, pred in enumerate(predictions):
            # 1. Confidence-based uncertainty
            max_confidence = np.max(pred)
            
            # 2. Entropy-based uncertainty
            entropy = -np.sum(pred * np.log(pred + 1e-10))
            
            # 3. Margin-based uncertainty
            sorted_pred = np.sort(pred)[::-1]
            margin = sorted_pred[0] - sorted_pred[1]
            
            # Aggregate uncertainty score
            uncertainty_score = (1 - max_confidence) * 0.4 + entropy * 0.3 + (1 - margin) * 0.3
            
            if uncertainty_score > self.uncertainty_threshold:
                uncertain_samples.append({
                    'sample_id': f"uncertain_{datetime.utcnow().timestamp()}_{i}",
                    'image': images[i],
                    'prediction': pred.tolist(),
                    'uncertainty_score': float(uncertainty_score),
                    'max_confidence': float(max_confidence),
                    'entropy': float(entropy),
                    'margin': float(margin),
                    'metadata': metadata[i],
                    'timestamp': datetime.utcnow().isoformat()
                })
        
        self.uncertain_samples.extend(uncertain_samples)
        logger.info(f"Identified {len(uncertain_samples)} uncertain samples")
        
        return uncertain_samples
    
    def add_labeled_sample(self, sample_id: str, true_label: int, 
                          reviewer_id: str, confidence: float = 1.0):
        """Add human-labeled sample to training pool"""
        # Find the sample
        sample = next((s for s in self.uncertain_samples 
                      if s['sample_id'] == sample_id), None)
        
        if sample:
            labeled_sample = {
                **sample,
                'true_label': true_label,
                'reviewer_id': reviewer_id,
                'review_confidence': confidence,
                'review_timestamp': datetime.utcnow().isoformat()
            }
            self.labeled_pool.append(labeled_sample)
            
            # Remove from uncertain pool
            self.uncertain_samples = [s for s in self.uncertain_samples 
                                     if s['sample_id'] != sample_id]
            
            logger.info(f"Sample {sample_id} added to labeled pool")
            return True
        return False
    
    def get_samples_for_review(self, n: int = 10, strategy: str = 'uncertainty') -> List[Dict]:
        """
        Get top N samples for human review
        Strategies: uncertainty, random, diverse
        """
        if strategy == 'uncertainty':
            sorted_samples = sorted(
                self.uncertain_samples,
                key=lambda x: x['uncertainty_score'],
                reverse=True
            )
            return sorted_samples[:n]
        
        elif strategy == 'random':
            indices = np.random.choice(
                len(self.uncertain_samples),
                min(n, len(self.uncertain_samples)),
                replace=False
            )
            return [self.uncertain_samples[i] for i in indices]
        
        elif strategy == 'diverse':
            # Implement diversity-based sampling
            return self._diverse_sampling(n)
        
        return []
    
    def _diverse_sampling(self, n: int) -> List[Dict]:
        """Select diverse samples using clustering"""
        if len(self.uncertain_samples) <= n:
            return self.uncertain_samples
        
        # Use predictions as features for diversity
        features = np.array([s['prediction'] for s in self.uncertain_samples])
        
        # Simple diversity: select samples with maximum distance
        selected_indices = [0]  # Start with first sample
        
        for _ in range(min(n - 1, len(features) - 1)):
            max_min_dist = -1
            best_idx = -1
            
            for i in range(len(features)):
                if i in selected_indices:
                    continue
                
                # Calculate minimum distance to already selected samples
                min_dist = min([np.linalg.norm(features[i] - features[j]) 
                               for j in selected_indices])
                
                if min_dist > max_min_dist:
                    max_min_dist = min_dist
                    best_idx = i
            
            if best_idx != -1:
                selected_indices.append(best_idx)
        
        return [self.uncertain_samples[i] for i in selected_indices]
    
    def prepare_retraining_data(self) -> Dict:
        """Prepare data for model retraining"""
        if len(self.labeled_pool) < 100:
            logger.warning("Insufficient labeled samples for retraining")
            return None
        
        images = [s['image'] for s in self.labeled_pool]
        labels = [s['true_label'] for s in self.labeled_pool]
        
        return {
            'images': images,
            'labels': labels,
            'sample_count': len(images),
            'timestamp': datetime.utcnow().isoformat()
        }
    
    def get_statistics(self) -> Dict:
        """Get active learning statistics"""
        return {
            'uncertain_samples_count': len(self.uncertain_samples),
            'labeled_samples_count': len(self.labeled_pool),
            'avg_uncertainty_score': float(np.mean([s['uncertainty_score'] 
                                                    for s in self.uncertain_samples])) 
                                     if self.uncertain_samples else 0,
            'ready_for_retraining': len(self.labeled_pool) >= 100
        }