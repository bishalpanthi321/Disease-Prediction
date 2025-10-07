"""
Analytics API Endpoints
"""
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from datetime import datetime
import logging

from backend.database import get_db
from backend.core.security import get_current_user
from backend.models.prediction import PredictionLog
from backend.models.feedback import UserFeedback
from backend.services.model_service import get_model_manager

router = APIRouter(prefix="/analytics", tags=["analytics"])
logger = logging.getLogger(__name__)

@router.get("/model-metrics")
async def get_model_metrics(
    user_id: str = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get model performance metrics"""
    try:
        model_manager = get_model_manager()
        total_predictions = db.query(PredictionLog).count()
        feedbacks = db.query(UserFeedback).count()
        
        # Calculate accuracy from feedback
        correct_predictions = db.query(UserFeedback).filter(
            UserFeedback.correct_class == PredictionLog.predicted_class
        ).count() if feedbacks > 0 else 0
        
        accuracy = correct_predictions / feedbacks if feedbacks > 0 else 1.0
        
        return {
            "model_version": model_manager.model_version,
            "total_predictions": total_predictions,
            "user_feedbacks": feedbacks,
            "estimated_accuracy": accuracy,
            "timestamp": datetime.utcnow().isoformat()
        }
    except Exception as e:
        logger.error(f"Analytics error: {e}")
        raise HTTPException(status_code=500, detail=str(e))