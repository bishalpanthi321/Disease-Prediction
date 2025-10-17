"""
Monitoring Dashboard - Generate Reports and Alerts
"""

from datetime import datetime
import json
import logging
from typing import Dict

logger = logging.getLogger(__name__)


class MonitoringDashboard:
    """
    Generate monitoring reports and alerts
    """
    
    def __init__(self, monitor, al_manager):
        self.monitor = monitor
        self.al_manager = al_manager
    
    def generate_report(self, period_days: int = 7) -> Dict:
        """Generate comprehensive monitoring report"""
        performance_summary = self.monitor.get_performance_summary(period_days)
        al_stats = self.al_manager.get_statistics()
        should_retrain, retrain_reason = self.monitor.should_retrain()
        
        report = {
            'report_date': datetime.utcnow().isoformat(),
            'period_days': period_days,
            'performance_summary': performance_summary,
            'active_learning': al_stats,
            'drift_alerts': self.monitor.drift_alerts[-10:],  # Last 10 alerts
            'retraining_recommendation': {
                'should_retrain': should_retrain,
                'reason': retrain_reason
            },
            'model_health': self._assess_model_health(performance_summary, al_stats)
        }
        
        return report
    
    def _assess_model_health(self, performance: Dict, al_stats: Dict) -> str:
        """Assess overall model health"""
        if 'avg_accuracy' not in performance:
            return "UNKNOWN"
        
        accuracy = performance['avg_accuracy']
        trend = performance.get('trend', 'STABLE')
        
        if accuracy > 0.90 and trend in ['STABLE', 'IMPROVING']:
            return "HEALTHY"
        elif accuracy > 0.80 and trend != 'DEGRADING':
            return "FAIR"
        elif accuracy > 0.70:
            return "DEGRADED"
        else:
            return "CRITICAL"
    
    def export_report(self, report: Dict, filename: str = None):
        """Export report to JSON file"""
        if filename is None:
            filename = f"monitoring_report_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}.json"
        
        with open(filename, 'w') as f:
            json.dump(report, f, indent=2)
        
        logger.info(f"Report exported to {filename}")
        return filename