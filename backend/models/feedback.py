"""
User Feedback Database Model
"""
from sqlalchemy import Column, String, DateTime
from datetime import datetime
from backend.database import Base

class UserFeedback(Base):
    __tablename__ = "user_feedback"
    
    id = Column(String, primary_key=True)
    prediction_id = Column(String, index=True)
    user_id = Column(String)
    correct_class = Column(String)
    timestamp = Column(DateTime, default=datetime.utcnow)
    comments = Column(String, nullable=True)