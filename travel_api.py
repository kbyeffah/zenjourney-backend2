from fastapi import FastAPI, Response
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime
import random
import json
from pydantic import BaseModel

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class TravelRequest(BaseModel):
    destination: str
    start_date: str
    end_date: str
    budget: float
    preferences: str

def get_random_weather():
    return f"{random.randint(15, 30)}°C, {random.choice(['Sunny', 'Partly Cloudy', 'Cloudy', 'Rainy'])}"

def get_random_hotel():
    return random.choice([
        "Grand Hotel",
        "City View Inn",
        "Riverside Hotel",
        "Central Plaza",
        "Garden Resort"
    ])

def get_random_restaurant():
    return random.choice([
        "Local Bistro",
        "Traditional Tavern",
        "Gourmet Restaurant",
        "Street Food Market",
        "Café Central"
    ])

def get_random_attraction():
    return random.choice([
        "Historic Castle",
        "Art Museum",
        "Botanical Garden",
        "City Center",
        "Local Market"
    ])

def get_random_event():
    return random.choice([
        "Art Gallery Exhibition",
        "Local Music Festival",
        "Food Market",
        "Cultural Show",
        "Historical Tour"
    ])

def create_daily_plan(day_number):
    return {
        "weather": get_random_weather(),
        "breakfast": f"{get_random_restaurant()} - Local Breakfast",
        "must_visit": f"{get_random_attraction()} - Less crowded in the morning",
        "local_event": get_random_event(),
        "dinner": f"{get_random_restaurant()} - Local Specialties",
        "hotel_suggestion": get_random_hotel(),
        "travel_distance": f"{random.randint(5, 20)} km from hotel"
    }

@app.post("/travel/plan")
async def create_travel_plan(request: TravelRequest):
    try:
        # Calculate number of days
        start = datetime.strptime(request.start_date, "%Y-%m-%d")
        end = datetime.strptime(request.end_date, "%Y-%m-%d")
        total_days = (end - start).days + 1
        
        # Generate daily plans
        daily_plans = {}
        for day in range(1, total_days + 1):
            daily_plans[f"Day {day}"] = create_daily_plan(day)
        
        # Create response
        response = {
            "destination": request.destination,
            "itinerary": daily_plans,
            "estimated_cost": request.budget * 0.9,  # 90% of budget
            "total_days": total_days
        }
        
        return response
        
    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001) 