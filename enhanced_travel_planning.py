#!/usr/bin/env python3
from uagents import Agent, Bureau, Context, Model
from datetime import datetime, timedelta
import json
import os
import uvicorn
from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from fetch_ai_agent import FetchAIAgent

# Initialize Fetch AI Agent
fetch_ai = FetchAIAgent()

# ----- Message Models -----

class TravelRequest(Model):
    destination: str
    start_date: str
    end_date: str
    budget: float
    preferences: str

class TravelPlan(Model):
    destination: str
    itinerary: str
    estimated_cost: float
    calendar_events: list = []  # New field for calendar events

class WeatherRequest(Model):
    destination: str
    start_date: str
    end_date: str

class WeatherResponse(Model):
    destination: str
    forecast: str
    avg_temp: float
    clothing_suggestions: str

class BudgetRequest(Model):
    destination: str
    total_budget: float
    duration_days: int

class BudgetResponse(Model):
    accommodation_budget: float
    food_budget: float
    transportation_budget: float
    activities_budget: float
    shopping_budget: float
    breakdown: str

class PhotoSpotsRequest(Model):
    destination: str

class PhotoSpotsResponse(Model):
    spots: str

class DietaryRequest(Model):
    destination: str
    preferences: str

class DietaryResponse(Model):
    recommendations: str

class TransportationRequest(Model):
    destination: str
    duration_days: int

class TransportationResponse(Model):
    recommendations: str
    estimated_cost: float

class EventsRequest(Model):
    destination: str
    start_date: str
    end_date: str

class EventsResponse(Model):
    events: str

# ----- Agent Definitions -----

travel_agent = Agent(
    name="travel_planner",
    port=8001,
    endpoint=["https://zenjourney.onrender.com/submit"],
)

weather_agent = Agent(
    name="weather_advisor",
    port=8002,
    endpoint=["http://localhost:8002/submit"],
)

budget_agent = Agent(
    name="budget_planner",
    port=8003,
    endpoint=["http://localhost:8003/submit"],
)

photo_spots_agent = Agent(
    name="photo_spots_finder",
    port=8004,
    endpoint=["http://localhost:8004/submit"],
)

dietary_agent = Agent(
    name="dietary_planner",
    port=8005,
    endpoint=["http://localhost:8005/submit"],
)

transportation_agent = Agent(
    name="transportation_advisor",
    port=8006,
    endpoint=["http://localhost:8006/submit"],
)

events_agent = Agent(
    name="events_finder",
    port=8007,
    endpoint=["http://localhost:8007/submit"],
)

# ----- Travel Agent Handlers -----

@travel_agent.on_event("startup")
async def travel_agent_startup(ctx: Context):
    ctx.logger.info(f"Travel Planning Agent started with address: {travel_agent.address}")

@travel_agent.on_message(model=TravelRequest)
async def handle_travel_request(ctx: Context, sender: str, msg: TravelRequest):
    try:
        # Parse dates
        start_date = datetime.strptime(msg.start_date, "%Y-%m-%d")
        end_date = datetime.strptime(msg.end_date, "%Y-%m-%d")
        
        # Create calendar events for the trip
        calendar_event = await fetch_ai.create_calendar_event(
            title=f"Trip to {msg.destination}",
            start_time=start_date,
            end_time=end_date,
            description=f"Travel plan with budget: ${msg.budget}"
        )
        
        # Create agentic workflow for the trip
        workflow_steps = [
            {"step": "weather_check", "agent": "weather_agent"},
            {"step": "budget_planning", "agent": "budget_agent"},
            {"step": "transportation", "agent": "transportation_agent"},
            {"step": "events", "agent": "events_agent"},
            {"step": "dietary", "agent": "dietary_agent"},
            {"step": "photo_spots", "agent": "photo_spots_agent"}
        ]
        
        workflow = await fetch_ai.create_agentic_workflow(
            workflow_name=f"Travel_Plan_{msg.destination}_{start_date.date()}",
            steps=workflow_steps
        )
        
        # Execute the workflow
        await fetch_ai.execute_workflow(workflow.get("workflow_id"))
        
        # Calculate trip duration in days
        duration_days = (end_date - start_date).days + 1
        
        # Request weather information
        ctx.logger.info("Requesting weather information...")
        weather_req = WeatherRequest(
            destination=msg.destination,
            start_date=msg.start_date,
            end_date=msg.end_date
        )
        weather_resp, weather_status = await ctx.send_and_receive(
            weather_agent.address, weather_req, response_type=WeatherResponse
        )
        
        # Request budget breakdown
        ctx.logger.info("Requesting budget breakdown...")
        budget_req = BudgetRequest(
            destination=msg.destination,
            total_budget=msg.budget,
            duration_days=duration_days
        )
        budget_resp, budget_status = await ctx.send_and_receive(
            budget_agent.address, budget_req, response_type=BudgetResponse
        )
        
        # Request photo spots
        ctx.logger.info("Requesting photo spots...")
        photo_req = PhotoSpotsRequest(destination=msg.destination)
        photo_resp, photo_status = await ctx.send_and_receive(
            photo_spots_agent.address, photo_req, response_type=PhotoSpotsResponse
        )
        
        # Request dietary recommendations
        ctx.logger.info("Requesting dietary recommendations...")
        diet_req = DietaryRequest(
            destination=msg.destination,
            preferences=msg.preferences
        )
        diet_resp, diet_status = await ctx.send_and_receive(
            dietary_agent.address, diet_req, response_type=DietaryResponse
        )
        
        # Request transportation options
        ctx.logger.info("Requesting transportation options...")
        transport_req = TransportationRequest(
            destination=msg.destination,
            duration_days=duration_days
        )
        transport_resp, transport_status = await ctx.send_and_receive(
            transportation_agent.address, transport_req, response_type=TransportationResponse
        )
        
        # Request local events
        ctx.logger.info("Requesting local events...")
        events_req = EventsRequest(
            destination=msg.destination,
            start_date=msg.start_date,
            end_date=msg.end_date
        )
        events_resp, events_status = await ctx.send_and_receive(
            events_agent.address, events_req, response_type=EventsResponse
        )
        
        # Compile the comprehensive travel plan
        itinerary = f"""
TRAVEL PLAN FOR {msg.destination.upper()}
{msg.start_date} to {msg.end_date} ({duration_days} days)

WEATHER FORECAST:
{weather_resp.forecast if isinstance(weather_resp, WeatherResponse) else "Weather information unavailable"}

PACKING SUGGESTIONS:
{weather_resp.clothing_suggestions if isinstance(weather_resp, WeatherResponse) else "Packing suggestions unavailable"}

BUDGET BREAKDOWN (Total: ${msg.budget:.2f}):
{budget_resp.breakdown if isinstance(budget_resp, BudgetResponse) else "Budget breakdown unavailable"}

MUST-VISIT PHOTO SPOTS:
{photo_resp.spots if isinstance(photo_resp, PhotoSpotsResponse) else "Photo spot recommendations unavailable"}

FOOD RECOMMENDATIONS:
{diet_resp.recommendations if isinstance(diet_resp, DietaryResponse) else "Dietary recommendations unavailable"}

TRANSPORTATION:
{transport_resp.recommendations if isinstance(transport_resp, TransportationResponse) else "Transportation recommendations unavailable"}

LOCAL EVENTS DURING YOUR STAY:
{events_resp.events if isinstance(events_resp, EventsResponse) else "Event information unavailable"}

ITINERARY SUGGESTIONS:

Day 1: Arrival and Settling In
- Arrive at {msg.destination}
- Check in to accommodation
- Local neighborhood exploration
- Dinner at a local restaurant based on your preferences

Days 2-{duration_days-1}:
- Mix of popular attractions and photo spots
- Local cuisine exploration
- Special events happening during your stay
- Cultural experiences based on your preferences

Day {duration_days}: Departure
- Final sightseeing or shopping
- Check out and departure

NOTES:
- This plan is customized based on your preferences: {msg.preferences}
- Estimated total cost: ${msg.budget:.2f}
- For detailed day-by-day planning, consult with a local tour guide
"""
        
        estimated_cost = msg.budget
        if isinstance(transport_resp, TransportationResponse):
            # Adjust with actual transportation cost estimate
            estimated_cost = min(estimated_cost, msg.budget)
        
        # Create the final travel plan
        travel_plan = TravelPlan(
            destination=msg.destination,
            itinerary=itinerary,
            estimated_cost=estimated_cost,
            calendar_events=[calendar_event]
        )
        
        # Return the plan to the sender
        await ctx.send(sender, travel_plan)
        
    except Exception as e:
        await ctx.send(sender, {"error": str(e)})

# ----- Travel Agent REST API -----

# Create the FastAPI app
app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Define the request model for the API
class TravelPlanRequest(Model):
    destination: str
    start_date: str
    end_date: str
    budget: float
    preferences: str

# Define the response model for the API
class TravelPlanResponse(Model):
    destination: str
    itinerary: str
    estimated_cost: float

@travel_agent.on_rest_post("/travel/plan", TravelPlanRequest, TravelPlanResponse)
async def handle_travel_plan_request(ctx: Context, request: TravelPlanRequest):
    ctx.logger.info(f"Received REST travel plan request for {request.destination}")
    
    # Convert REST request to internal message
    travel_req = TravelRequest(
        destination=request.destination,
        start_date=request.start_date,
        end_date=request.end_date,
        budget=request.budget,
        preferences=request.preferences
    )
    
    # Send to self and get response
    travel_resp, status = await ctx.send_and_receive(
        travel_agent.address, travel_req, response_type=TravelPlan
    )
    
    if not isinstance(travel_resp, TravelPlan):
        ctx.logger.error(f"Failed to generate travel plan: {status}")
        return TravelPlanResponse(
            destination=request.destination,
            itinerary="Failed to generate travel plan. Please try again later.",
            estimated_cost=request.budget
        )
    
    return TravelPlanResponse(
        destination=travel_resp.destination,
        itinerary=travel_resp.itinerary,
        estimated_cost=travel_resp.estimated_cost
    )

if __name__ == "__main__":
    # Create a bureau and add all agents
    bureau = Bureau()
    bureau.add(travel_agent)
    bureau.add(weather_agent)
    bureau.add(budget_agent)
    bureau.add(photo_spots_agent)
    bureau.add(dietary_agent)
    bureau.add(transportation_agent)
    bureau.add(events_agent)
    
    # Run all agents
    bureau.run() 