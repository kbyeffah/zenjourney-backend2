from uagents import Agent, Context
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime
import random
from models import pydantic_models
import os
from uvicorn import Config, Server

# Initialize FastAPI app
app = FastAPI()

# Configure CORS to allow frontend requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3001",  # Local frontend
        "https://*.vercel.app",  # Vercel frontend
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize uAgent
planning_agent = Agent(
    name='Travel Planning Agent',
    port=8001,
    endpoint={"http://localhost:8001/submit": {"weight": 1}},
    network=None
)

# FastAPI endpoint for travel planning
@app.post("/travel/plan")
async def handle_travel_plan(request: pydantic_models["TravelRequest"]):
    try:
        destination = request.destination
        start_date = request.start_date
        end_date = request.end_date
        budget = request.budget
        preferences = request.preferences

        start = datetime.strptime(start_date, "%Y-%m-%d")
        end = datetime.strptime(end_date, "%Y-%m-%d")
        total_days = (end - start).days + 1

        daily_plans = {}
        for day in range(1, total_days + 1):
            daily_plans[f"Day {day}"] = create_daily_plan(day)

        response = {
            "destination": destination,
            "itinerary": daily_plans,
            "estimated_cost": budget * 0.9,
            "hotel_suggestions": [get_random_hotel() for _ in range(3)],
            "total_days": total_days
        }
        return response
    except Exception as e:
        return {"error": str(e)}

# Utility functions
def get_random_weather():
    return f"{random.randint(15, 30)}°C, {random.choice(['Sunny', 'Cloudy', 'Rainy'])}"

def get_random_hotel():
    return random.choice(["Grand Hotel", "City View Inn", "Riverside Hotel"])

def get_random_restaurant():
    return random.choice(["Local Bistro", "Gourmet Restaurant", "Café Central"])

def get_random_attraction():
    return random.choice(["Art Museum", "Botanical Garden", "City Center"])

def get_random_event():
    return random.choice(["Music Festival", "Cultural Show", "Historical Tour"])

def create_daily_plan(day_number):
    return {
        "weather": get_random_weather(),
        "breakfast": f"{get_random_restaurant()} - Local Breakfast",
        "must_visit": f"{get_random_attraction()} - Less crowded",
        "local_event": get_random_event(),
        "dinner": f"{get_random_restaurant()} - Local Specialties",
        "hotel_suggestion": get_random_hotel(),
        "travel_distance": f"{random.randint(5, 20)} km"
    }

# Agent startup and message handling
@planning_agent.on_event('startup')
async def startup_handler(ctx: Context):
    ctx.logger.info(f'Travel Planning Agent started with address: {ctx.agent.address}')

@planning_agent.on_message(model=pydantic_models["TravelRequest"])
async def handle_travel_request(ctx: Context, sender: str, msg: pydantic_models["TravelRequest"]):
    ctx.logger.info(f"Received travel request: {msg.destination}")
    plan = create_travel_plan(msg)
    travel_plan = pydantic_models["TravelPlan"](
        destination=plan["destination"],
        itinerary=plan["itinerary"],
        estimated_cost=plan["estimated_cost"],
        hotel_suggestions=plan["hotel_suggestions"],
        total_days=plan["total_days"]
    )
    await ctx.send(sender, travel_plan)

def create_travel_plan(request: pydantic_models["TravelRequest"]) -> dict:
    start_date = datetime.strptime(request.start_date, "%Y-%m-%d")
    end_date = datetime.strptime(request.end_date, "%Y-%m-%d")
    total_days = (end_date - start_date).days + 1
    daily_plans = {}
    for day in range(1, total_days + 1):
        daily_plans[f"Day {day}"] = create_daily_plan(day)
    hotel_suggestions = [get_random_hotel() for _ in range(3)]
    estimated_cost = request.budget * 0.9
    return {
        "destination": request.destination,
        "itinerary": daily_plans,
        "estimated_cost": estimated_cost,
        "hotel_suggestions": hotel_suggestions,
        "total_days": total_days
    }

# Run FastAPI server
if __name__ == "__main__":
    config = Config(
        app=app,
        host="0.0.0.0",
        port=int(os.getenv("PORT", 8001)),
        log_level="info"
    )
    server = Server(config)
    server.run()