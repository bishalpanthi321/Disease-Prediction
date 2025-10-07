"""
Prediction Database Models
"""
from sqlalchemy import Column, String, Float, DateTime, JSON, Integer
from datetime import datetime
from backend.database import Base

class PredictionLog(Base):
    __tablename__ = "prediction_logs"
    
    id = Column(String, primary_key=True)
    user_id = Column(String, index=True)
    timestamp = Column(DateTime, default=datetime.utcnow)
    predicted_class = Column(String)
    confidence = Column(Float)
    corrected_class = Column(String, nullable=True)
    metadata = Column(JSON)
    image_path = Column(String)
    severity = Column(String)
    treatment_plan = Column(JSON)