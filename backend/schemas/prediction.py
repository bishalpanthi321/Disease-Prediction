"""
Prediction Request/Response Schemas
"""
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any

class PredictionRequest(BaseModel):
    metadata: Optional[Dict[str, Any]] = Field(default_factory=dict)
    include_explainability: bool = False
    include_treatment: bool = True

class PredictionResponse(BaseModel):
    prediction_id: str
    predicted_class: str
    confidence: float
    severity: str
    all_probabilities: Dict[str, float]
    treatment_suggestions: Optional[List[Dict[str, Any]]] = None
    explainability: Optional[Dict[str, Any]] = None
    metadata: Dict[str, Any]

class TreatmentSuggestion(BaseModel):
    name: str
    type: str  # chemical, organic, cultural
    dosage: str
    cost_estimate: float
    effectiveness: float
    side_effects: List[str]
    application_method: str