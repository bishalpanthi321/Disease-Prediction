"""
Feedback Schemas
"""
from pydantic import BaseModel
from typing import Optional

class FeedbackRequest(BaseModel):
    prediction_id: str
    correct_class: str
    comments: Optional[str] = None

class FeedbackResponse(BaseModel):
    message: str
    feedback_id: str