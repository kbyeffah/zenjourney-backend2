from pydantic import BaseModel, field_validator
from typing import Dict, List, Union

class TravelRequest(BaseModel):
    destination: str
    start_date: str
    end_date: str
    budget: float
    preferences: Union[str, List[str]]
    
    @field_validator('preferences')
    @classmethod
    def validate_preferences(cls, v):
        if isinstance(v, list):
            return ", ".join(v)  # Convert list to comma-separated string
        return v  # Return string as-is

class DailyPlan(BaseModel):
    weather: str
    breakfast: str
    must_visit: str
    local_event: str
    dinner: str
    hotel_suggestion: str
    travel_distance: str

class TravelPlan(BaseModel):
    destination: str
    itinerary: Dict[str, DailyPlan]
    estimated_cost: float
    hotel_suggestions: List[str]
    total_days: int

pydantic_models = {
    "TravelRequest": TravelRequest,
    "TravelPlan": TravelPlan,
    "DailyPlan": DailyPlan
}