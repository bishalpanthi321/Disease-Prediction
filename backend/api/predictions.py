"""
Prediction API Endpoints
"""
from fastapi import APIRouter, File, UploadFile, HTTPException, Depends
from sqlalchemy.orm import Session
from PIL import Image
import io
import json
import uuid
from datetime import datetime
import logging

from backend.database import get_db
from backend.core.security import get_current_user
from backend.core.cache import get_redis_client
from backend.schemas.prediction import PredictionResponse
from backend.services.model_service import get_model_manager
from backend.services.treatment_service import get_treatment_suggestions
from backend.services.explainability import generate_explainability_map
from backend.models.prediction import PredictionLog
from backend.config import CLASS_NAMES

router = APIRouter(prefix="/predict", tags=["predictions"])
logger = logging.getLogger(__name__)

@router.post("/", response_model=PredictionResponse)
async def predict_disease(
    file: UploadFile = File(...),
    metadata: str = '{}',
    include_explainability: bool = False,
    include_treatment: bool = True,
    user_id: str = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Main prediction endpoint with metadata support
    """
    prediction_id = str(uuid.uuid4())
    redis_client = get_redis_client()
    model_manager = get_model_manager()
    
    try:
        # Parse metadata
        meta_dict = json.loads(metadata)
        
        # Check cache
        cache_key = f"prediction:{file.filename}"
        cached = redis_client.get(cache_key)
        if cached:
            logger.info("Returning cached prediction")
            return json.loads(cached)
        
        # Read and process image
        contents = await file.read()
        image = Image.open(io.BytesIO(contents)).convert('RGB')
        
        # Make prediction
        predicted_class, confidence, all_probs = model_manager.predict(image)
        
        # Estimate severity
        severity = model_manager.estimate_severity(predicted_class, confidence, meta_dict)
        
        # Get treatment suggestions
        treatments = None
        if include_treatment:
            treatments = get_treatment_suggestions(predicted_class)
        
        # Generate explainability
        explainability = None
        if include_explainability:
            processed_img = model_manager.preprocess_image(image)
            predicted_idx = CLASS_NAMES.index(predicted_class)
            heatmap = generate_explainability_map(
                processed_img, 
                model_manager.model, 
                predicted_idx
            )
            explainability = {
                "heatmap": heatmap,
                "method": "grad_cam",
                "explanation": f"Areas highlighted show regions influencing the {predicted_class} prediction"
            }
        
        # Prepare response
        response = PredictionResponse(
            prediction_id=prediction_id,
            predicted_class=predicted_class,
            confidence=confidence,
            severity=severity,
            all_probabilities=all_probs,
            treatment_suggestions=treatments,
            explainability=explainability,
            metadata={
                **meta_dict,
                "model_version": model_manager.model_version,
                "timestamp": datetime.utcnow().isoformat()
            }
        )
        
        # Log prediction to database
        log_entry = PredictionLog(
            id=prediction_id,
            user_id=user_id,
            predicted_class=predicted_class,
            confidence=confidence,
            metadata=meta_dict,
            image_path=f"storage/{prediction_id}.jpg",
            severity=severity,
            treatment_plan=treatments
        )
        db.add(log_entry)
        db.commit()
        
        # Cache result
        redis_client.setex(
            cache_key,
            3600,  # 1 hour
            json.dumps(response.dict())
        )
        
        return response
        
    except Exception as e:
        logger.error(f"Prediction error: {e}")
        raise HTTPException(status_code=500, detail=str(e))