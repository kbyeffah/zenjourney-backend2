from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv
import google.generativeai as genai
import logging
import json
import random
import jwt
from typing import List, Dict

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
logger.info(f"Gemini API Key {'is set' if api_key else 'is not set'}")

# Configure Gemini
if api_key:
    genai.configure(api_key=api_key)
    try:
        # List available models
        available_models = genai.list_models()
        logger.info("Available Gemini models:")
        for m in available_models:
            logger.info(f"Model: {m.name}, Supported methods: {m.supported_generation_methods}")
        
        # Use the latest Gemini Pro model
        model = genai.GenerativeModel("gemini-1.0-pro")
        logger.info("Successfully configured Gemini model")
    except Exception as e:
        logger.error(f"Error configuring Gemini: {str(e)}")
        logger.error(f"Error details: {e.__class__.__name__}")
        if hasattr(e, 'response'):
            logger.error(f"Response: {e.response}")
        model = None

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

class Analytics(BaseModel):
    total_calls: int
    average_duration: float
    common_questions: List[Dict[str, str | int]]
    
    class Config:
        arbitrary_types_allowed = True

def generate_random_travel_plan(destination, start_date, end_date, budget, preferences):
    """Generate a travel plan with random data when OpenAI API fails"""
    start = datetime.strptime(start_date, "%Y-%m-%d")
    end = datetime.strptime(end_date, "%Y-%m-%d")
    total_days = (end - start).days + 1
    
    # Generate daily plans
    daily_plans = {}
    for day in range(1, total_days + 1):
        daily_plans[f"Day {day}"] = {
            "weather": f"{random.randint(20, 30)}°C, {random.choice(['Sunny', 'Partly Cloudy', 'Cloudy'])}",
            "breakfast": f"{random.choice(['Local Cafe', 'Hotel Restaurant', 'Street Food'])} - {random.choice(['Traditional', 'International', 'Healthy'])} Breakfast",
            "must_visit": {
                "attraction": random.choice(['Historic Site', 'Museum', 'Park', 'Market', 'Beach']),
                "crowd_info": random.choice(['Less crowded in morning', 'Popular spot', 'Quiet area']),
                "recommended_time": random.choice(['Morning', 'Afternoon', 'Evening'])
            },
            "local_event": {
                "name": random.choice(['Cultural Festival', 'Food Market', 'Art Exhibition', 'Music Show']),
                "type": random.choice(['Cultural', 'Entertainment', 'Food']),
                "duration": random.choice(['2 hours', '4 hours', 'All day']),
                "venue": random.choice(['City Center', 'Local Park', 'Convention Center'])
            },
            "dinner": f"{random.choice(['Local Restaurant', 'Fine Dining', 'Street Food'])} - {random.choice(['Traditional', 'International', 'Fusion'])} Cuisine",
            "travel_tips": {
                "morning_activity": random.choice(['Visit early', 'Book in advance', 'Wear comfortable shoes']),
                "transport": random.choice(['Public transport', 'Taxi', 'Walking']),
                "local_customs": random.choice(['Dress modestly', 'Remove shoes', 'Greet locals'])
            }
        }
    
    # Generate hotel suggestions
    hotel_suggestions = [
        {
            "name": random.choice(['Grand Hotel', 'City View Inn', 'Riverside Hotel', 'Central Plaza']),
            "rating": random.randint(3, 5),
            "price_per_night": random.randint(50, 200),
            "amenities": random.sample(['WiFi', 'Pool', 'Gym', 'Restaurant', 'Spa'], 3),
            "location": random.choice(['City Center', 'Near Beach', 'Business District'])
        } for _ in range(3)
    ]
    
    # Calculate estimated cost
    estimated_cost = sum(hotel['price_per_night'] for hotel in hotel_suggestions[:1]) * total_days * 1.5
    
    return {
        "destination": destination,
        "total_days": total_days,
        "itinerary": daily_plans,
        "hotel_suggestions": hotel_suggestions,
        "estimated_cost": estimated_cost,
        "travel_tips": {
            "best_time_to_visit": random.choice(['Spring', 'Autumn', 'Winter']),
            "local_transportation": random.choice(['Metro', 'Bus', 'Taxi']),
            "currency": random.choice(['USD', 'EUR', 'Local Currency']),
            "language": random.choice(['English', 'Local Language']),
            "emergency_numbers": {
                "police": "911",
                "ambulance": "911",
                "tourist_helpline": "1-800-TOURISM"
            }
        }
    }

def generate_travel_plan_with_gemini(destination, start_date, end_date, budget, preferences):
    logger.info(f"Starting Gemini travel plan generation for {destination}")
    
    if not api_key:
        logger.error("Gemini API key not found in environment variables")
        return generate_random_travel_plan(destination, start_date, end_date, budget, preferences)
    
    try:
        prompt = f"""Create a detailed travel itinerary for {destination} from {start_date} to {end_date} with a budget of {budget} euros.
        Preferences: {preferences}
        
        Create a unique and personalized travel plan that includes local attractions, events, and restaurants specific to {destination}.
        Consider the dates {start_date} to {end_date} when suggesting activities and events.
        The total cost should not exceed {budget} euros.
        Focus on {preferences} experiences.
        
        Format the response as a JSON object with this exact structure:
        {{
            "destination": "{destination}",
            "total_days": number,
            "itinerary": {{
                "Day 1": {{
                    "weather": "string",
                    "breakfast": "string",
                    "must_visit": {{
                        "attraction": "string",
                        "crowd_info": "string",
                        "recommended_time": "string"
                    }},
                    "local_event": {{
                        "name": "string",
                        "type": "string",
                        "duration": "string",
                        "venue": "string"
                    }},
                    "dinner": "string",
                    "travel_tips": {{
                        "morning_activity": "string",
                        "transport": "string",
                        "local_customs": "string"
                    }}
                }}
            }},
            "hotel_suggestions": [
                {{
                    "name": "string",
                    "rating": number,
                    "price_per_night": number,
                    "amenities": ["string"],
                    "location": "string"
                }}
            ],
            "estimated_cost": number,
            "travel_tips": {{
                "best_time_to_visit": "string",
                "local_transportation": "string",
                "currency": "string",
                "language": "string",
                "emergency_numbers": {{
                    "police": "string",
                    "ambulance": "string",
                    "tourist_helpline": "string"
                }}
            }}
        }}
        """
        
        logger.info("Sending request to Gemini API")
        response = model.generate_content(prompt)
        
        logger.info("Received response from Gemini API")
        logger.debug(f"Raw response: {response.text}")
        
        # Try to extract JSON from the response
        try:
            # Find the first { and last } to extract the JSON
            start = response.text.find('{')
            end = response.text.rfind('}') + 1
            if start != -1 and end != 0:
                json_str = response.text[start:end]
                logger.debug(f"Extracted JSON: {json_str}")
                plan = json.loads(json_str)
            else:
                raise ValueError("No JSON object found in response")
        except json.JSONDecodeError as e:
            logger.error(f"JSON parsing error: {str(e)}")
            logger.error(f"Response text: {response.text}")
            raise
        
        logger.info(f"Generated plan for {destination}: {json.dumps(plan, indent=2)}")
        return plan
        
    except Exception as e:
        logger.error(f"Error in generate_travel_plan_with_gemini: {str(e)}")
        logger.info("Falling back to random travel plan generation")
        return generate_random_travel_plan(destination, start_date, end_date, budget, preferences)

@app.post("/travel/plan")
async def create_travel_plan(request: TravelRequest):
    logger.info(f"Received request for {request.destination}")
    try:
        # Calculate number of days for validation
        start = datetime.strptime(request.start_date, "%Y-%m-%d")
        end = datetime.strptime(request.end_date, "%Y-%m-%d")
        if end < start:
            raise HTTPException(status_code=400, detail="End date must be after start date")
        
        # Generate travel plan using Gemini or fallback to random
        plan = generate_travel_plan_with_gemini(
            request.destination,
            request.start_date,
            request.end_date,
            request.budget,
            request.preferences
        )
        
        logger.info(f"Successfully generated plan for {request.destination}")
        return plan
        
    except Exception as e:
        logger.error(f"Error processing request: {str(e)}")
        if isinstance(e, HTTPException):
            raise e
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/admin/analytics")
async def get_analytics(credentials: HTTPAuthorizationCredentials = Depends(HTTPBearer())):
    try:
        # Verify JWT token
        token = credentials.credentials
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        
        # Check if user is admin
        if not payload.get("is_admin"):
            raise HTTPException(status_code=403, detail="Not authorized")
        
        # Get analytics from database
        analytics = {
            "total_calls": 150,  # Replace with actual database query
            "average_duration": 5.5,  # Replace with actual database query
            "common_questions": [
                {"question": "How do I reset my password?", "count": 45},
                {"question": "What are your business hours?", "count": 32},
                {"question": "How do I update my profile?", "count": 28},
                {"question": "Where can I find my order history?", "count": 25},
                {"question": "How do I contact support?", "count": 20}
            ]
        }
        
        return analytics
        
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 