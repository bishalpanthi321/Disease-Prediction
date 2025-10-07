"""
Treatment Service - Treatment recommendations
"""
from typing import List, Dict

# Treatment Database (simplified - should be in database)
TREATMENT_DATABASE = {
    "Apple___Apple_scab": [
        {
            "name": "Captan Fungicide",
            "type": "chemical",
            "dosage": "2-3 lbs per 100 gallons",
            "cost_estimate": 45.0,
            "effectiveness": 0.85,
            "side_effects": ["May affect beneficial insects"],
            "application_method": "Spray every 7-10 days"
        },
        {
            "name": "Neem Oil",
            "type": "organic",
            "dosage": "2 tablespoons per gallon",
            "cost_estimate": 15.0,
            "effectiveness": 0.65,
            "side_effects": ["Minimal"],
            "application_method": "Spray weekly"
        }
    ],
    "Tomato___Late_blight": [
        {
            "name": "Copper Fungicide",
            "type": "chemical",
            "dosage": "1-2 lbs per acre",
            "cost_estimate": 35.0,
            "effectiveness": 0.80,
            "side_effects": ["Can accumulate in soil"],
            "application_method": "Apply at first sign, repeat every 5-7 days"
        }
    ]
    # Add more treatments for other diseases
}

def get_treatment_suggestions(disease_class: str) -> List[Dict]:
    """Get treatment suggestions for a disease"""
    return TREATMENT_DATABASE.get(disease_class, [])