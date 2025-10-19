"""
Advanced Interactive Monitoring System with Report Generation
Includes trend analysis, anomaly detection, predictive alerts, and interactive dashboard
"""

import numpy as np
import pandas as pd
from datetime import datetime, timedelta
import json
from collections import defaultdict
from enum import Enum
import logging

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class AlertSeverity(Enum):
    """Alert severity levels"""
    INFO = "ℹ️ INFO"
    WARNING = "⚠️ WARNING"
    CRITICAL = "🚨 CRITICAL"
    SUCCESS = "✅ SUCCESS"


class InteractiveMonitoringSystem:
    """Advanced monitoring system with interactive features"""
    
    def __init__(self, monitor, al_manager, retraining_pipeline):
        self.monitor = monitor
        self.al_manager = al_manager
        self.retraining = retraining_pipeline
        self.alerts_history = []
        self.recommendations = []
        self.performance_trends = defaultdict(list)
        self.anomaly_scores = []
        self.user_feedback_buffer = []
        
    def run_interactive_session(self):
        """Run interactive monitoring session with menu-driven interface"""
        print("\n" + "="*80)
        print("🔬 ADVANCED PLANT DISEASE DETECTION - MONITORING SYSTEM 🔬".center(80))
        print("="*80 + "\n")
        
        while True:
            self._display_main_menu()
            choice = input("\n📋 Select option (1-8): ").strip()
            
            if choice == '1':
                self._simulate_production_data()
            elif choice == '2':
                self._analyze_model_performance()
            elif choice == '3':
                self._analyze_drift_detection()
            elif choice == '4':
                self._review_active_learning()
            elif choice == '5':
                self._analyze_anomalies()
            elif choice == '6':
                self._generate_advanced_report()
            elif choice == '7':
                self._interactive_alerts_dashboard()
            elif choice == '8':
                self._export_full_analysis()
                print("\n✅ Exiting monitoring system. Goodbye!")
                break
            else:
                print("❌ Invalid option. Please try again.")
    
    def _display_main_menu(self):
        """Display main menu options"""
        print("\n" + "-"*80)
        print("MAIN MENU - SELECT AN OPTION:")
        print("-"*80)
        print("1️⃣  Simulate Production Data (Generate realistic monitoring data)")
        print("2️⃣  Analyze Model Performance (Detailed metrics and trends)")
        print("3️⃣  Analyze Drift Detection (Distribution shifts and anomalies)")
        print("4️⃣  Review Active Learning (Uncertain samples & labeling progress)")
        print("5️⃣  Analyze Anomalies (Detect outliers and unusual patterns)")
        print("6️⃣  Generate Advanced Report (Comprehensive analysis & recommendations)")
        print("7️⃣  Alerts Dashboard (Real-time monitoring alerts)")
        print("8️⃣  Exit (Export and quit)")
        print("-"*80)
    
    def _simulate_production_data(self):
        """Simulate realistic production data with multiple days"""
        print("\n🔄 Simulating Production Data...\n")
        
        days = 7
        for day in range(days):
            print(f"📅 Day {day + 1}/{days}:", end=" ")
            
            # Simulate daily predictions
            daily_predictions = np.random.randint(0, 38, size=500)
            daily_labels = np.random.randint(0, 38, size=500)
            
            # Add some correlation (realistic)
            accuracy_variance = np.sin(day / 2) * 0.05
            match_indices = np.random.choice(500, int(500 * (0.88 + accuracy_variance)), replace=False)
            daily_labels[match_indices] = daily_predictions[match_indices]
            
            # Track performance
            perf = self.monitor.track_performance(
                daily_predictions.tolist(),
                daily_labels.tolist(),
                {'day': day + 1, 'predictions_count': len(daily_predictions)}
            )
            
            self.performance_trends['accuracy'].append(perf['accuracy'])
            self.performance_trends['f1_score'].append(perf['f1_score'])
            self.performance_trends['timestamp'].append(perf['timestamp'])
            
            print(f"✅ Accuracy: {perf['accuracy']:.2%} | F1: {perf['f1_score']:.2%}")
        
        print("\n✅ Production data simulation complete!\n")
    
    def _analyze_model_performance(self):
        """Detailed performance analysis"""
        print("\n📊 DETAILED MODEL PERFORMANCE ANALYSIS")
        print("="*80)
        
        if not self.monitor.performance_history:
            print("❌ No performance data available. Run option 1 first.")
            return
        
        # Get summary
        summary = self.monitor.get_performance_summary(days=7)
        
        print(f"\n📈 7-Day Performance Summary:")
        print(f"   • Total Predictions: {summary['total_predictions']:,}")
        print(f"   • Average Accuracy: {summary['avg_accuracy']:.2%}")
        print(f"   • Average F1 Score: {summary['avg_f1']:.2%}")
        print(f"   • Accuracy Std Dev: {summary['accuracy_std']:.4f}")
        print(f"   • Min Accuracy: {summary['min_accuracy']:.2%}")
        print(f"   • Max Accuracy: {summary['max_accuracy']:.2%}")
        print(f"   • Trend: {summary['trend']}")
        
        # Detailed trend analysis
        print(f"\n🔍 Trend Analysis:")
        if summary['trend'] == 'IMPROVING':
            print("   ✅ Model performance is IMPROVING")
            self.alerts_history.append({
                'severity': AlertSeverity.SUCCESS,
                'message': 'Model performance improving',
                'timestamp': datetime.utcnow().isoformat()
            })
        elif summary['trend'] == 'DEGRADING':
            print("   ⚠️  Model performance is DEGRADING - Retraining may be needed")
            self.alerts_history.append({
                'severity': AlertSeverity.WARNING,
                'message': 'Model performance degrading',
                'timestamp': datetime.utcnow().isoformat()
            })
        else:
            print("   ℹ️  Model performance is STABLE")
        
        # Accuracy distribution
        accuracies = [p['accuracy'] for p in self.monitor.performance_history[-7:]]
        print(f"\n📉 Accuracy Distribution (Last 7 records):")
        for i, acc in enumerate(accuracies, 1):
            bar = "█" * int(acc * 50)
            print(f"   Day {i}: {bar} {acc:.2%}")
        
        # Performance comparison
        if len(self.monitor.performance_history) >= 10:
            recent_5 = np.mean([p['accuracy'] for p in self.monitor.performance_history[-5:]])
            older_5 = np.mean([p['accuracy'] for p in self.monitor.performance_history[-10:-5]])
            change = recent_5 - older_5
            
            print(f"\n🔄 Performance Change (Recent vs. Historical):")
            print(f"   • Last 5 records avg: {recent_5:.2%}")
            print(f"   • Previous 5 records avg: {older_5:.2%}")
            print(f"   • Change: {change:+.2%}")
    
    def _analyze_drift_detection(self):
        """Comprehensive drift analysis"""
        print("\n🌊 DRIFT DETECTION ANALYSIS")
        print("="*80)
        
        if not self.monitor.baseline_distribution:
            print("\n⚠️  Setting baseline from current data...")
            baseline_preds = np.random.rand(100, 38)
            dummy_labels = np.zeros(100, dtype=int)
            self.monitor.set_baseline(baseline_preds, dummy_labels)
        
        # Generate current predictions with some drift
        print("\n🔄 Simulating production predictions...\n")
        
        current_preds = np.random.rand(200, 38) + 0.05  # Slight drift
        drift_report = self.monitor.detect_drift(current_preds)
        
        print(f"📊 Drift Metrics:")
        print(f"   • Population Stability Index (PSI): {drift_report['psi']:.4f}")
        print(f"   • Kolmogorov-Smirnov p-value: {drift_report['ks_pvalue']:.4f}")
        print(f"   • Jensen-Shannon Divergence: {drift_report['js_divergence']:.4f}")
        print(f"   • Drift Detected: {'✅ YES' if drift_report['drift_detected'] else '❌ NO'}")
        print(f"   • Severity Level: {drift_report['severity']}")
        
        # Drift interpretation
        print(f"\n🔍 Drift Interpretation:")
        if drift_report['severity'] == 'CRITICAL':
            print("   🚨 CRITICAL DRIFT - Model retraining URGENT!")
            self.alerts_history.append({
                'severity': AlertSeverity.CRITICAL,
                'message': 'Critical drift detected - immediate retraining recommended',
                'timestamp': datetime.utcnow().isoformat()
            })
        elif drift_report['severity'] == 'HIGH':
            print("   ⚠️  HIGH DRIFT - Monitor closely and plan retraining")
            self.alerts_history.append({
                'severity': AlertSeverity.WARNING,
                'message': 'High drift detected',
                'timestamp': datetime.utcnow().isoformat()
            })
        else:
            print("   ✅ LOW DRIFT - Model performing as expected")
        
        # Historical drift alerts
        print(f"\n📋 Recent Drift Alerts (Last 5):")
        for i, alert in enumerate(self.monitor.drift_alerts[-5:], 1):
            print(f"   {i}. {alert['severity']} - PSI: {alert['psi']:.4f} ({alert['timestamp'][:10]})")
    
    def _review_active_learning(self):
        """Review active learning progress"""
        print("\n🎓 ACTIVE LEARNING REVIEW")
        print("="*80)
        
        # Identify uncertain samples
        print("\n🔄 Identifying uncertain samples...\n")
        predictions = np.random.rand(300, 38)
        uncertain_samples = self.al_manager.identify_uncertain_samples(
            predictions,
            [f"image_{i}" for i in range(300)],
            [{'location': f'field_{i%3}'} for i in range(300)]
        )
        
        stats = self.al_manager.get_statistics()
        
        print(f"📊 Active Learning Statistics:")
        print(f"   • Uncertain Samples in Queue: {stats['uncertain_samples_count']}")
        print(f"   • Labeled Samples Collected: {stats['labeled_samples_count']}")
        print(f"   • Average Uncertainty Score: {stats['avg_uncertainty_score']:.4f}")
        print(f"   • Ready for Retraining: {'✅ YES' if stats['ready_for_retraining'] else '❌ NO'}")
        
        # Show top uncertain samples
        print(f"\n🎯 Top 5 Most Uncertain Samples for Review:")
        top_samples = self.al_manager.get_samples_for_review(n=5, strategy='uncertainty')
        for i, sample in enumerate(top_samples, 1):
            print(f"   {i}. Uncertainty Score: {sample['uncertainty_score']:.4f}")
            print(f"      Max Confidence: {sample['max_confidence']:.4f}")
            print(f"      Entropy: {sample['entropy']:.4f}")
        
        # Simulate labeling
        if top_samples:
            print(f"\n✏️  Simulating expert feedback on top 3 samples...")
            for i, sample in enumerate(top_samples[:3], 1):
                self.al_manager.add_labeled_sample(
                    sample['sample_id'],
                    true_label=np.random.randint(0, 38),
                    reviewer_id='expert_panel',
                    confidence=0.95
                )
                print(f"   ✅ Sample {i} labeled and added to training pool")
        
        # Check retraining readiness
        updated_stats = self.al_manager.get_statistics()
        if updated_stats['ready_for_retraining']:
            print(f"\n🎉 Active learning pool has reached {updated_stats['labeled_samples_count']} samples!")
            print(f"   Ready for model retraining cycle.")
            self.recommendations.append({
                'priority': 'HIGH',
                'action': 'Trigger model retraining with collected labeled samples',
                'reason': f'Accumulated {updated_stats["labeled_samples_count"]} labeled samples'
            })
    
    def _analyze_anomalies(self):
        """Detect anomalies in performance metrics"""
        print("\n🔎 ANOMALY DETECTION ANALYSIS")
        print("="*80)
        
        if len(self.monitor.performance_history) < 5:
            print("⚠️  Need at least 5 performance records for anomaly detection.")
            return
        
        accuracies = np.array([p['accuracy'] for p in self.monitor.performance_history])
        
        # Calculate anomaly scores using Z-score
        mean_acc = np.mean(accuracies)
        std_acc = np.std(accuracies)
        z_scores = np.abs((accuracies - mean_acc) / (std_acc + 1e-8))
        
        print(f"\n📊 Performance Anomalies (Z-score > 2):")
        print(f"   Mean Accuracy: {mean_acc:.2%}")
        print(f"   Std Deviation: {std_acc:.4f}")
        
        anomalies_found = False
        for i, z in enumerate(z_scores):
            if z > 2:
                anomalies_found = True
                record = self.monitor.performance_history[i]
                print(f"\n   🚨 Anomaly at record {i+1}:")
                print(f"      Accuracy: {record['accuracy']:.2%} (Z-score: {z:.2f})")
                print(f"      Timestamp: {record['timestamp']}")
                print(f"      Sample Size: {record['sample_size']}")
                
                self.alerts_history.append({
                    'severity': AlertSeverity.WARNING,
                    'message': f'Performance anomaly detected - accuracy {record["accuracy"]:.2%}',
                    'timestamp': record['timestamp']
                })
        
        if not anomalies_found:
            print("   ✅ No significant anomalies detected - Performance stable")
    
    def _generate_advanced_report(self):
        """Generate comprehensive monitoring report"""
        print("\n📄 GENERATING ADVANCED MONITORING REPORT")
        print("="*80)
        
        print("\n⏳ Analyzing all metrics...\n")
        
        # Compile all data
        perf_summary = self.monitor.get_performance_summary(days=7) if self.monitor.performance_history else {}
        al_stats = self.al_manager.get_statistics()
        should_retrain, reason = self.monitor.should_retrain()
        
        report = {
            'timestamp': datetime.utcnow().isoformat(),
            'system_status': self._determine_system_status(),
            'performance': perf_summary,
            'active_learning': al_stats,
            'drift_status': {
                'drift_alerts_count': len(self.monitor.drift_alerts),
                'last_alert': self.monitor.drift_alerts[-1] if self.monitor.drift_alerts else None
            },
            'retraining_recommendation': {
                'should_retrain': should_retrain,
                'reason': reason
            },
            'alerts_count': len(self.alerts_history),
            'recommendations': self.recommendations
        }
        
        # Display report
        print("📊 SYSTEM HEALTH SCORECARD:")
        print(f"   Overall Status: {report['system_status']}")
        print(f"   Performance: {perf_summary.get('avg_accuracy', 'N/A')}")
        print(f"   Drift Alerts: {report['drift_status']['drift_alerts_count']}")
        print(f"   Active Alerts: {report['alerts_count']}")
        print(f"   Retraining Needed: {'✅ YES' if should_retrain else '❌ NO'}")
        
        print(f"\n📋 RECOMMENDATIONS:")
        if self.recommendations:
            for i, rec in enumerate(self.recommendations, 1):
                print(f"   {i}. [{rec['priority']}] {rec['action']}")
                print(f"      Reason: {rec['reason']}")
        else:
            print("   ✅ No critical actions needed at this time")
        
        # Export to file
        filename = f"monitoring_report_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}.json"
        with open(filename, 'w') as f:
            json.dump(report, f, indent=2, default=str)
        
        print(f"\n✅ Report exported to: {filename}\n")
    
    def _interactive_alerts_dashboard(self):
        """Display interactive alerts dashboard"""
        print("\n🚨 REAL-TIME ALERTS DASHBOARD")
        print("="*80)
        
        if not self.alerts_history:
            print("\n✅ No alerts currently. System operating normally.\n")
            return
        
        # Group alerts by severity
        alerts_by_severity = defaultdict(list)
        for alert in self.alerts_history:
            alerts_by_severity[alert['severity']].append(alert)
        
        # Display alerts
        print(f"\n📊 Alert Summary:")
        print(f"   Total Alerts: {len(self.alerts_history)}")
        print(f"   Critical: {len(alerts_by_severity[AlertSeverity.CRITICAL])}")
        print(f"   Warnings: {len(alerts_by_severity[AlertSeverity.WARNING])}")
        print(f"   Info: {len(alerts_by_severity[AlertSeverity.INFO])}")
        
        print(f"\n🔔 Recent Alerts (Last 10):")
        for i, alert in enumerate(self.alerts_history[-10:], 1):
            print(f"   {i}. {alert['severity'].value} {alert['message']}")
    
    def _export_full_analysis(self):
        """Export complete analysis"""
        print("\n💾 EXPORTING FULL ANALYSIS")
        print("="*80)
        
        analysis = {
            'timestamp': datetime.utcnow().isoformat(),
            'performance_history': self.monitor.performance_history,
            'drift_alerts': self.monitor.drift_alerts,
            'active_learning_stats': self.al_manager.get_statistics(),
            'all_alerts': self.alerts_history,
            'recommendations': self.recommendations
        }
        
        filename = f"full_analysis_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}.json"
        with open(filename, 'w') as f:
            json.dump(analysis, f, indent=2, default=str)
        
        print(f"\n✅ Full analysis exported to: {filename}")
        print(f"   • Performance records: {len(self.monitor.performance_history)}")
        print(f"   • Drift alerts: {len(self.monitor.drift_alerts)}")
        print(f"   • Total alerts: {len(self.alerts_history)}")
        print(f"   • Recommendations: {len(self.recommendations)}\n")
    
    def _determine_system_status(self) -> str:
        """Determine overall system status"""
        if len(self.alerts_history) > 5:
            return "🔴 CRITICAL"
        elif len(self.monitor.drift_alerts) > 2:
            return "🟡 WARNING"
        elif self.monitor.performance_history and np.mean([p['accuracy'] for p in self.monitor.performance_history]) < 0.85:
            return "🟡 ATTENTION"
        else:
            return "🟢 HEALTHY"


# Main execution
if __name__ == "__main__":
    from monitoring.prometheus import ModelMonitor, ActiveLearningManager, RetrainingPipeline
    
    # Initialize components
    monitor = ModelMonitor(drift_threshold=0.15)
    al_manager = ActiveLearningManager(uncertainty_threshold=0.7)
    retraining_pipeline = RetrainingPipeline(
        model_path='trained_model.keras',
        data_dir='data'
    )
    
    # Start interactive monitoring
    system = InteractiveMonitoringSystem(monitor, al_manager, retraining_pipeline)
    system.run_interactive_session()