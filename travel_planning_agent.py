from uagents import Agent, Context, Model
from fastapi import FastAPI, Response
from datetime import datetime, timedelta
import random
import json
from models import TravelRequest, DailyPlan, TravelPlan

# Create planning agent
planning_agent = Agent(
    name='Travel Planning Agent',
    port=8001,
    endpoint=['http://localhost:8001/submit'],
    network=None  # Disable Fetch.ai network for local testing
)

# Create FastAPI app instance
app = FastAPI()

# Configure FastAPI app with CORS
@planning_agent.on_event("startup")
async def setup_fastapi(ctx: Context):
    from fastapi.middleware.cors import CORSMiddleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # In production, specify actual origins
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    @app.post("/travel/plan")
    async def handle_travel_plan(request: dict):
        try:
            # Extract request parameters
            destination = request.get("destination", "")
            start_date = request.get("start_date", "")
            end_date = request.get("end_date", "")
            budget = float(request.get("budget", 0))
            preferences = request.get("preferences", "")
            
            # Calculate number of days
            start = datetime.strptime(start_date, "%Y-%m-%d")
            end = datetime.strptime(end_date, "%Y-%m-%d")
            total_days = (end - start).days + 1
            
            # Generate daily plans
            daily_plans = {}
            for day in range(1, total_days + 1):
                daily_plans[f"Day {day}"] = create_daily_plan(day)
            
            # Create response
            response = {
                "destination": destination,
                "itinerary": daily_plans,
                "estimated_cost": budget * 0.9,  # 90% of budget
                "hotel_suggestions": [get_random_hotel() for _ in range(3)],
                "total_days": total_days
            }
            
            return response
            
        except Exception as e:
            return {"error": str(e)}

@planning_agent.on_event('startup')
async def startup_handler(ctx: Context):
    ctx.logger.info(f'Travel Planning Agent started with address: {ctx.agent.address}')

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

def create_travel_plan(request: TravelRequest) -> dict:
    """Generate a detailed travel plan based on the request"""
    start_date = datetime.strptime(request.start_date, "%Y-%m-%d")
    end_date = datetime.strptime(request.end_date, "%Y-%m-%d")
    total_days = (end_date - start_date).days + 1
    daily_plans = {}
    for day in range(1, total_days + 1):
        daily_plans[f"Day {day}"] = create_daily_plan(day)
    hotel_suggestions = [get_random_hotel() for _ in range(3)]
    estimated_cost = request.budget * 0.9  # Use 90% of budget
    return {
        "destination": request.destination,
        "itinerary": daily_plans,
        "estimated_cost": estimated_cost,
        "hotel_suggestions": hotel_suggestions,
        "total_days": total_days
    }

@planning_agent.on_message(model=TravelRequest)
async def handle_travel_request(ctx: Context, sender: str, msg: TravelRequest):
    ctx.logger.info(f"Received travel request: {msg.destination}")
    plan = create_travel_plan(msg)
    travel_plan = TravelPlan(
        destination=plan["destination"],
        itinerary=plan["itinerary"],
        estimated_cost=plan["estimated_cost"],
        hotel_suggestions=plan["hotel_suggestions"],
        total_days=plan["total_days"]
    )
    await ctx.send(sender, travel_plan)

if __name__ == "__main__":
    planning_agent.run()