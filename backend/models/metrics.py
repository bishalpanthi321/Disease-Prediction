"""
Model Metrics Database Model
"""
from sqlalchemy import Column, String, Float, DateTime, Integer
from datetime import datetime
from backend.database import Base

class ModelMetrics(Base):
    __tablename__ = "model_metrics"
    
    id = Column(String, primary_key=True)
    model_version = Column(String)
    timestamp = Column(DateTime, default=datetime.utcnow)
    accuracy = Column(Float)
    drift_score = Column(Float)
    total_predictions = Column(Integer)
    