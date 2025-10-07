"""
Common Schemas and Enums
"""
from enum import Enum

class SeverityLevel(str, Enum):
    HEALTHY = "healthy"
    MILD = "mild"
    MODERATE = "moderate"
    SEVERE = "severe"
    CRITICAL = "critical"