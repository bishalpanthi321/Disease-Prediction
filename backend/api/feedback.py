"""
Feedback API Endpoints
"""
from fastapi import APIRouter, HTTPException, Depends, BackgroundTasks
from sqlalchemy.orm import Session
import uuid
import logging

from backend.database import get_db
from backend.core.security import get_current_user
from backend.schemas.feedback import FeedbackRequest, FeedbackResponse
from backend.models.feedback import UserFeedback
from backend.models.prediction import PredictionLog

router = APIRouter(prefix="/feedback", tags=["feedback"])
logger = logging.getLogger(__name__)

def check_retraining_needed(db: Session):
    """Background task to check if model needs retraining"""
    try:
        from backend.config import RETRAINING_THRESHOLD
        feedback_count = db.query(UserFeedback).count()
        if feedback_count >= RETRAINING_THRESHOLD:
            logger.info("Retraining threshold reached. Triggering retraining...")
            # Implement retraining logic or send notification
    except Exception as e:
        logger.error(f"Retraining check error: {e}")

@router.post("/", response_model=FeedbackResponse)
async def submit_feedback(
    feedback: FeedbackRequest,
    user_id: str = Depends(get_current_user),
    db: Session = Depends(get_db),
    background_tasks: BackgroundTasks = None
):
    """
    Submit feedback for active learning
    """
    try:
        feedback_entry = UserFeedback(
            id=str(uuid.uuid4()),
            prediction_id=feedback.prediction_id,
            user_id=user_id,
            correct_class=feedback.correct_class,
            comments=feedback.comments
        )
        db.add(feedback_entry)
        
        # Update prediction log
        pred_log = db.query(PredictionLog).filter(
            PredictionLog.id == feedback.prediction_id
        ).first()
        if pred_log:
            pred_log.corrected_class = feedback.correct_class
        
        db.commit()
        
        # Trigger retraining check in background
        if background_tasks:
            background_tasks.add_task(check_retraining_needed, db)
        
        return FeedbackResponse(
            message="Feedback received",
            feedback_id=feedback_entry.id
        )
    except Exception as e:
        logger.error(f"Feedback error: {e}")
        raise HTTPException(status_code=500, detail=str(e))
    