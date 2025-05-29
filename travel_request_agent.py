from uagents import Agent, Context
from models import TravelRequest, TravelPlan
import json

# Create travel request agent
request_agent = Agent(
    name='Travel Request Agent',
    port=8000,
    endpoint=['http://localhost:8000/submit'],
    network=None  # Disable Fetch.ai network for local testing
)

# Planning agent address from your latest logs
planning_agent_address = "agent1q29pszep92xpjlz25jnjlu99nkfc79fggmtevkkth5n876t2gfywu3xd59c"

@request_agent.on_event('startup')
async def startup_handler(ctx: Context):
    ctx.logger.info(f'Travel Request Agent started with address: {ctx.agent.address}')

@request_agent.on_interval(period=10.0)  # Send a request every 10 seconds
async def send_travel_request(ctx: Context):
    ctx.logger.info("Sending travel request to planning agent...")
    
    # Create a travel request
    request = TravelRequest(
        destination="Tokyo, Japan",
        start_date="2023-07-01",
        end_date="2023-07-10",
        budget=2500.0,
        preferences="Cultural experiences, good food, technology"
    )
    
    # Send the request (response is handled by on_message)
    try:
        await ctx.send(planning_agent_address, request)
        ctx.logger.info("Travel request sent, waiting for response...")
    except Exception as e:
        ctx.logger.error(f'Error sending travel request: {str(e)}')

@request_agent.on_message(model=TravelPlan)
async def handle_travel_plan(ctx: Context, sender: str, msg: TravelPlan):
    ctx.logger.info(f'Received travel plan from {sender}:')
    ctx.logger.info(f'Destination: {msg.destination}')
    ctx.logger.info(f'Itinerary: {json.dumps(msg.itinerary, indent=2)}')
    ctx.logger.info(f'Estimated cost: ${msg.estimated_cost}')
    ctx.logger.info(f'Hotel suggestions: {msg.hotel_suggestions}')
    ctx.logger.info(f'Total days: {msg.total_days}')

if __name__ == "__main__":
    request_agent.run()