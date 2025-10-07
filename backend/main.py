"""
FastAPI Backend for Plant Disease Prediction System
Main application entry point
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import logging

from backend.config import API_TITLE, API_VERSION, API_DESCRIPTION, CORS_ORIGINS, LOG_LEVEL
from backend.database import engine, SessionLocal, Base
from backend.core.cache import get_redis_client
from backend.api import predictions, feedback, analytics
from backend.services.model_service import get_model_manager

# Logging Configuration
logging.basicConfig(level=LOG_LEVEL)
logger = logging.getLogger(__name__)

# Create database tables
Base.metadata.create_all(bind=engine)

# Initialize FastAPI
app = FastAPI(
    title=API_TITLE,
    version=API_VERSION,
    description=API_DESCRIPTION
)

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(predictions.router)
app.include_router(feedback.router)
app.include_router(analytics.router)

# Root endpoint
@app.get("/")
async def root():
    return {
        "message": "Plant Disease Prediction API",
        "version": API_VERSION,
        "status": "operational"
    }

# Health check endpoint
@app.get("/health")
async def health_check():
    """Health check endpoint for monitoring"""
    try:
        # Check model
        model_manager = get_model_manager()
        model_status = model_manager.model is not None
        
        # Check database
        db = SessionLocal()
        db.execute("SELECT 1")
        db.close()
        db_status = True
        
        # Check Redis
        redis_client = get_redis_client()
        redis_client.ping()
        cache_status = True
        
        return {
            "status": "healthy",
            "model": model_status,
            "database": db_status,
            "cache": cache_status,
            "timestamp": datetime.utcnow().isoformat()
        }
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        raise HTTPException(status_code=503, detail="Service unhealthy")

if __name__ == "__main__":
    import uvicorn
    from datetime import datetime
    from fastapi import HTTPException
    uvicorn.run(app, host="0.0.0.0", port=8000)