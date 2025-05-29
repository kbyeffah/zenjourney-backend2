from uagents import Model

class TravelRequest(Model):
    destination: str
    start_date: str
    end_date: str
    budget: float
    preferences: str

class DailyPlan(Model):
    weather: str
    breakfast: str
    must_visit: str
    local_event: str
    dinner: str
    hotel_suggestion: str
    travel_distance: str

class TravelPlan(Model):
    destination: str
    itinerary: dict
    estimated_cost: float
    hotel_suggestions: list
    total_days: int