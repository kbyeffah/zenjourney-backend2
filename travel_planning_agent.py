from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import random
from pydantic import BaseModel
import pandas as pd

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://localhost:3001",
        "http://zenjourney-frontend.vercel.app",
        "https://*.vercel.app",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic models to match TravelPlanDisplay.tsx
class MustVisit(BaseModel):
    attraction: str
    crowd_info: str
    recommended_time: str

class LocalEvent(BaseModel):
    name: str
    type: str
    duration: str

class TravelTips(BaseModel):
    morning_activity: str
    transport: str
    local_customs: str

class DailyPlan(BaseModel):
    weather: str
    breakfast: str
    must_visit: MustVisit
    local_event: LocalEvent
    dinner: str
    travel_tips: TravelTips

class EmergencyNumbers(BaseModel):
    police: str
    ambulance: str
    tourist_helpline: str

class GeneralTravelTips(BaseModel):
    best_time_to_visit: str
    local_transportation: str
    currency: str
    language: str
    emergency_numbers: EmergencyNumbers

class HotelSuggestion(BaseModel):
    name: str
    rating: float
    price_per_night: float
    amenities: list[str]
    location: str

class TravelPlan(BaseModel):
    destination: str
    itinerary: dict[str, DailyPlan]
    estimated_cost: float
    hotel_suggestions: list[HotelSuggestion]
    travel_tips: GeneralTravelTips

# Mock data generation
def create_must_visit() -> MustVisit:
    attractions = ["Eiffel Tower", "Louvre Museum", "Central Park", "Tokyo Tower"]
    return MustVisit(
        attraction=random.choice(attractions),
        crowd_info="Moderate crowds expected",
        recommended_time="9:00 AM - 12:00 PM"
    )

def create_local_event() -> LocalEvent:
    events = ["Summer Festival", "Art Exhibition", "Local Market Day"]
    return LocalEvent(
        name=random.choice(events),
        type="Cultural",
        duration="2-3 hours"
    )

def create_travel_tips() -> TravelTips:
    return TravelTips(
        morning_activity="Visit local markets",
        transport="Public metro or taxi",
        local_customs="Greet with a bow in Japan"
    )

def create_daily_plan() -> DailyPlan:
    return DailyPlan(
        weather="Sunny, 25°C",
        breakfast="Croissants and coffee",
        must_visit=create_must_visit(),
        local_event=create_local_event(),
        dinner="Local seafood restaurant",
        travel_tips=create_travel_tips()
    )

def create_hotel_suggestion() -> HotelSuggestion:
    hotels = ["Grand Hotel", "Seaside Inn", "City Center Suites"]
    return HotelSuggestion(
        name=random.choice(hotels),
        rating=round(random.uniform(3.5, 5.0), 1),
        price_per_night=round(random.uniform(100, 300), 2),
        amenities=["Wi-Fi", "Pool", "Breakfast Included"],
        location="Downtown"
    )

def create_general_travel_tips() -> GeneralTravelTips:
    return GeneralTravelTips(
        best_time_to_visit="Spring (March-May)",
        local_transportation="Metro and taxis",
        currency="USD",
        language="English",
        emergency_numbers=EmergencyNumbers(
            police="911",
            ambulance="911",
            tourist_helpline="1-800-555-1234"
        )
    )

def create_travel_plan(destination: str, total_days: int) -> TravelPlan:
    itinerary = {f"Day {i+1}": create_daily_plan() for i in range(total_days)}
    return TravelPlan(
        destination=destination,
        itinerary=itinerary,
        estimated_cost=random.uniform(1000, 5000),
        hotel_suggestions=[create_hotel_suggestion() for _ in range(3)],
        travel_tips=create_general_travel_tips()
    )

# API endpoint
class TravelPlanRequest(BaseModel):
    destination: str
    start_date: str
    end_date: str
    budget: float
    preferences: str

@app.post("/travel/plan")
async def generate_travel_plan(request: TravelPlanRequest):
    total_days = (pd.to_datetime(request.end_date) - pd.to_datetime(request.start_date)).days + 1
    plan = create_travel_plan(request.destination, total_days)
    return plan