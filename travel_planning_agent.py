from fastapi import FastAPI, Header, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime
import random
from models import pydantic_models
import os
from uvicorn import Config, Server
from firebase_admin import auth, initialize_app, credentials
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize Firebase Admin SDK (ensure you have a service account JSON file)
try:
    cred = credentials.Certificate(os.getenv("FIREBASE_CREDENTIALS_PATH", "path/to/serviceAccountKey.json"))
    initialize_app(cred)
    logger.info("Firebase Admin SDK initialized successfully")
except Exception as e:
    logger.error(f"Failed to initialize Firebase Admin SDK: {e}")

# Initialize FastAPI app
app = FastAPI()

# Configure CORS to allow frontend requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "https://zenjourney.vercel.app",  # Replace with your actual Vercel URL
        "https://*.vercel.app",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Root endpoint
@app.get("/")
async def root():
    return {"message": "ZenJourney Travel Planning API"}

# FastAPI endpoint for travel planning
@app.post("/travel/plan")
async def handle_travel_plan(request: pydantic_models["TravelRequest"], authorization: str = Header(None)):
    try:
        # Validate Firebase token if provided
        if authorization:
            try:
                token = authorization.replace("Bearer ", "")
                auth.verify_id_token(token)
                logger.info("Firebase token verified successfully")
            except Exception as e:
                logger.error(f"Firebase token verification failed: {e}")
                raise HTTPException(status_code=401, detail="Invalid or expired token")

        destination = request.destination
        start_date = request.start_date
        end_date = request.end_date
        budget = request.budget
        preferences = request.preferences

        try:
            start = datetime.strptime(start_date, "%Y-%m-%d")
            end = datetime.strptime(end_date, "%Y-%m-%d")
        except ValueError as e:
            logger.error(f"Date parsing error: {e}")
            raise HTTPException(status_code=400, detail="Invalid date format. Use YYYY-MM-DD.")

        if start > end:
            raise HTTPException(status_code=400, detail="End date must be after start date")

        total_days = (end - start).days + 1
        if total_days <= 0:
            raise HTTPException(status_code=400, detail="Trip duration must be at least 1 day")

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
        logger.info(f"Generated travel plan for {destination} with {total_days} days")
        return response
    except HTTPException as he:
        raise he
    except Exception as e:
        logger.error(f"Error generating travel plan: {e}")
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")

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
        "must_visit": {
            "attraction": get_random_attraction(),
            "crowd_info": "Less crowded",
            "recommended_time": f"{random.randint(9, 12)} AM - {random.randint(1, 5)} PM"
        },
        "local_event": get_random_event(),
        "dinner": f"{get_random_restaurant()} - Local Specialties",
        "hotel_suggestion": get_random_hotel(),
        "travel_distance": f"{random.randint(5, 20)} km"
    }

# Run FastAPI server
if __name__ == "__main__":
    port = int(os.getenv("PORT", 8001))
    config = Config(
        app=app,
        host="0.0.0.0",
        port=port,
        log_level="info"
    )
    server = Server(config)
    logger.info(f"Starting FastAPI server on port {port}")
    server.run()