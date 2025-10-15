"""
Model Monitoring, Drift Detection, and Active Learning Pipeline
Detects performance degradation and triggers retraining
"""

import numpy as np
import pandas as pd
from sklearn.metrics import accuracy_score, precision_recall_fscore_support
from scipy import stats
from datetime import datetime, timedelta
import logging
from typing import Dict, List, Tuple

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ModelMonitor:
    """
    Monitors model performance and detects drift
    """
    
    def __init__(self, drift_threshold: float = 0.15, window_size: int = 1000):
        self.drift_threshold = drift_threshold
        self.window_size = window_size
        self.baseline_distribution = None
        self.performance_history = []
        self.drift_alerts = []
        
    def set_baseline(self, predictions: np.ndarray, labels: np.ndarray):
        """Set baseline distribution for drift detection"""
        self.baseline_distribution = {
            'predictions': predictions,
            'labels': labels,
            'mean': np.mean(predictions, axis=0),
            'std': np.std(predictions, axis=0),
            'timestamp': datetime.utcnow()
        }
        logger.info("Baseline distribution set")
    
    def detect_drift(self, current_predictions: np.ndarray) -> Dict:
        """
        Detect distribution drift using multiple methods
        """
        if self.baseline_distribution is None:
            logger.warning("Baseline not set, cannot detect drift")
            return {'drift_detected': False}
        
        baseline_mean = self.baseline_distribution['mean']
        baseline_std = self.baseline_distribution['std']
        
        current_mean = np.mean(current_predictions, axis=0)
        current_std = np.std(current_predictions, axis=0)
        
        # 1. Population Stability Index (PSI)
        psi = self._calculate_psi(baseline_mean, current_mean)
        
        # 2. Kolmogorov-Smirnov Test
        ks_statistic, ks_pvalue = stats.ks_2samp(
            baseline_mean.flatten(),
            current_mean.flatten()
        )
        
        # 3. Jensen-Shannon Divergence
        js_divergence = self._calculate_js_divergence(baseline_mean, current_mean)
        
        drift_detected = (
            psi > self.drift_threshold or
            ks_pvalue < 0.05 or
            js_divergence > 0.1
        )
        
        drift_report = {
            'drift_detected': drift_detected,
            'psi': float(psi),
            'ks_statistic': float(ks_statistic),
            'ks_pvalue': float(ks_pvalue),
            'js_divergence': float(js_divergence),
            'timestamp': datetime.utcnow().isoformat(),
            'severity': self._assess_drift_severity(psi, ks_pvalue, js_divergence)
        }
        
        if drift_detected:
            self.drift_alerts.append(drift_report)
            logger.warning(f"Drift detected! PSI: {psi:.4f}, KS p-value: {ks_pvalue:.4f}")
        
        return drift_report
    
    def _calculate_psi(self, baseline: np.ndarray, current: np.ndarray) -> float:
        """Calculate Population Stability Index"""
        epsilon = 1e-10
        psi = np.sum((current - baseline) * np.log((current + epsilon) / (baseline + epsilon)))
        return abs(psi)
    
    def _calculate_js_divergence(self, p: np.ndarray, q: np.ndarray) -> float:
        """Calculate Jensen-Shannon Divergence"""
        epsilon = 1e-10
        p = p + epsilon
        q = q + epsilon
        m = 0.5 * (p + q)
        
        kl_pm = np.sum(p * np.log(p / m))
        kl_qm = np.sum(q * np.log(q / m))
        
        return 0.5 * (kl_pm + kl_qm)
    
    def _assess_drift_severity(self, psi: float, ks_pvalue: float, js_div: float) -> str:
        """Assess drift severity level"""
        if psi > 0.25 or js_div > 0.2:
            return "CRITICAL"
        elif psi > 0.15 or js_div > 0.1:
            return "HIGH"
        elif psi > 0.10 or ks_pvalue < 0.05:
            return "MODERATE"
        else:
            return "LOW"
    
    def track_performance(self, predictions: List, true_labels: List, metadata: Dict):
        """Track model performance metrics over time"""
        accuracy = accuracy_score(true_labels, predictions)
        precision, recall, f1, _ = precision_recall_fscore_support(
            true_labels, predictions, average='weighted'
        )
        
        performance_record = {
            'timestamp': datetime.utcnow().isoformat(),
            'accuracy': float(accuracy),
            'precision': float(precision),
            'recall': float(recall),
            'f1_score': float(f1),
            'sample_size': len(predictions),
            'metadata': metadata
        }
        
        self.performance_history.append(performance_record)
        
        # Keep only recent history
        if len(self.performance_history) > 10000:
            self.performance_history = self.performance_history[-10000:]
        
        logger.info(f"Performance tracked - Accuracy: {accuracy:.4f}, F1: {f1:.4f}")
        
        return performance_record
    
    def get_performance_summary(self, days: int = 7) -> Dict:
        """Get performance summary for the last N days"""
        cutoff_date = datetime.utcnow() - timedelta(days=days)
        
        recent_performance = [
            p for p in self.performance_history
            if datetime.fromisoformat(p['timestamp']) > cutoff_date
        ]
        
        if not recent_performance:
            return {'message': 'No data available'}
        
        df = pd.DataFrame(recent_performance)
        
        return {
            'period_days': days,
            'total_predictions': int(df['sample_size'].sum()),
            'avg_accuracy': float(df['accuracy'].mean()),
            'avg_f1': float(df['f1_score'].mean()),
            'accuracy_std': float(df['accuracy'].std()),
            'min_accuracy': float(df['accuracy'].min()),
            'max_accuracy': float(df['accuracy'].max()),
            'trend': self._calculate_trend(df['accuracy'].values)
        }
    
    def _calculate_trend(self, values: np.ndarray) -> str:
        """Calculate performance trend"""
        if len(values) < 2:
            return "INSUFFICIENT_DATA"
        
        slope, _, _, p_value, _ = stats.linregress(range(len(values)), values)
        
        if p_value > 0.05:
            return "STABLE"
        elif slope > 0.001:
            return "IMPROVING"
        elif slope < -0.001:
            return "DEGRADING"
        else:
            return "STABLE"
    
    def should_retrain(self) -> Tuple[bool, str]:
        """Determine if model should be retrained"""
        reasons = []
        
        # Check for drift
        if len(self.drift_alerts) > 0:
            recent_drifts = [d for d in self.drift_alerts 
                           if datetime.fromisoformat(d['timestamp']) > 
                           datetime.utcnow() - timedelta(days=7)]
            if len(recent_drifts) >= 3:
                reasons.append("Multiple drift alerts detected")
        
        # Check performance degradation
        if len(self.performance_history) >= 10:
            recent_performance = self.performance_history[-10:]
            avg_recent_acc = np.mean([p['accuracy'] for p in recent_performance])
            
            if len(self.performance_history) >= 20:
                baseline_performance = self.performance_history[-20:-10]
                avg_baseline_acc = np.mean([p['accuracy'] for p in baseline_performance])
                
                if avg_recent_acc < avg_baseline_acc - 0.05:
                    reasons.append("Significant accuracy drop detected")
        
        should_retrain = len(reasons) > 0
        reason_str = "; ".join(reasons) if reasons else "No retraining needed"
        
        return should_retrain, reason_str