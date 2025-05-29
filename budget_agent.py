#!/usr/bin/env python3
from uagents import Agent, Context, Model

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

# Create the budget agent
budget_agent = Agent(
    name="budget_planner",
    port=8003,
    endpoint=["http://localhost:8003/submit"],
)

@budget_agent.on_event("startup")
async def startup(ctx: Context):
    ctx.logger.info(f"Budget Planner Agent started with address: {budget_agent.address}")

@budget_agent.on_message(model=BudgetRequest)
async def handle_budget_request(ctx: Context, sender: str, msg: BudgetRequest):
    ctx.logger.info(f"Received budget request for {msg.destination} with {msg.total_budget} USD budget for {msg.duration_days} days")
    
    # Calculate budget breakdown
    breakdown = calculate_budget(msg.destination, msg.total_budget, msg.duration_days)
    
    # Create and send the response
    response = BudgetResponse(
        accommodation_budget=breakdown["accommodation"],
        food_budget=breakdown["food"],
        transportation_budget=breakdown["transportation"],
        activities_budget=breakdown["activities"],
        shopping_budget=breakdown["shopping"],
        breakdown=breakdown["text"]
    )
    
    await ctx.send(sender, response)

def calculate_budget(destination, total_budget, duration_days):
    """Calculate budget breakdown based on destination, total budget, and duration."""
    destination = destination.lower()
    
    # Default budget allocation percentages
    allocations = {
        "accommodation": 0.35,  # 35% of budget
        "food": 0.25,           # 25% of budget
        "transportation": 0.15,  # 15% of budget
        "activities": 0.15,     # 15% of budget
        "shopping": 0.10        # 10% of budget
    }
    
    # Adjust allocations based on destination
    if "paris" in destination or "london" in destination or "new york" in destination:
        # More expensive cities - higher accommodation costs
        allocations = {
            "accommodation": 0.40,
            "food": 0.25,
            "transportation": 0.12,
            "activities": 0.13,
            "shopping": 0.10
        }
    elif "bangkok" in destination or "bali" in destination or "mexico" in destination:
        # Budget-friendly destinations - lower accommodation costs
        allocations = {
            "accommodation": 0.25,
            "food": 0.30,
            "transportation": 0.15,
            "activities": 0.20,
            "shopping": 0.10
        }
    elif "dubai" in destination or "tokyo" in destination:
        # Luxury destinations - higher food and shopping costs
        allocations = {
            "accommodation": 0.35,
            "food": 0.30,
            "transportation": 0.12,
            "activities": 0.13,
            "shopping": 0.10
        }
    
    # Calculate budget amounts
    budget_amounts = {}
    for category, percentage in allocations.items():
        budget_amounts[category] = total_budget * percentage
    
    # Calculate daily budgets
    daily_accommodation = budget_amounts["accommodation"] / duration_days
    daily_food = budget_amounts["food"] / duration_days
    daily_transportation = budget_amounts["transportation"] / duration_days
    daily_activities = budget_amounts["activities"] / duration_days
    daily_shopping = budget_amounts["shopping"] / duration_days
    
    # Create text breakdown
    text_breakdown = f"""
BUDGET BREAKDOWN (${total_budget:.2f} total for {duration_days} days):

Accommodation: ${budget_amounts['accommodation']:.2f} (${daily_accommodation:.2f}/day)
Food & Dining: ${budget_amounts['food']:.2f} (${daily_food:.2f}/day)
Transportation: ${budget_amounts['transportation']:.2f} (${daily_transportation:.2f}/day)
Activities & Attractions: ${budget_amounts['activities']:.2f} (${daily_activities:.2f}/day)
Shopping & Souvenirs: ${budget_amounts['shopping']:.2f} (${daily_shopping:.2f}/day)

RECOMMENDATIONS:
"""
    
    # Add recommendations based on the destination and budget
    if "paris" in destination:
        text_breakdown += """
- Save on accommodation by staying in neighborhoods like Montmartre or Le Marais
- Purchase a Paris Museum Pass for attractions if visiting multiple museums
- Use the Metro for transportation (cost-effective)
- Consider picnics in parks with local baguettes, cheese, and wine to save on some meals
"""
    elif "tokyo" in destination:
        text_breakdown += """
- Stay in business hotels or hostels for better rates
- Purchase a Tokyo Metro pass for unlimited travel
- Try affordable eateries like ramen shops and conveyor belt sushi
- Look for free attractions like parks and shrine visits
"""
    elif "bali" in destination:
        text_breakdown += """
- Consider homestays or guesthouses for authentic and affordable accommodation
- Rent a scooter for transportation if comfortable riding
- Eat at local warungs (small family-owned restaurants) for authentic and affordable meals
- Negotiate prices at markets for better deals on souvenirs
"""
    elif "new york" in destination:
        text_breakdown += """
- Consider staying in Brooklyn or Queens for more affordable accommodation
- Purchase a 7-day MetroCard for unlimited subway and bus travel
- Visit museums on free or pay-what-you-wish days
- Try food trucks and markets for affordable meals
"""
    else:
        text_breakdown += """
- Look for accommodations with kitchen facilities to save on meal costs
- Use public transportation where available
- Research free or low-cost attractions
- Consider a mix of dining out and self-catering for balanced food budget
"""
    
    # Add the budget amounts and text to the result
    result = budget_amounts.copy()
    result["text"] = text_breakdown
    
    return result

if __name__ == "__main__":
    budget_agent.run() 