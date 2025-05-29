#!/usr/bin/env python3
from uagents import Bureau
import enhanced_travel_planning

if __name__ == "__main__":
    # Create the bureau
    bureau = Bureau()
    
    # Add all agents to the bureau
    bureau.add(enhanced_travel_planning.travel_agent)
    bureau.add(enhanced_travel_planning.weather_agent)
    bureau.add(enhanced_travel_planning.budget_agent)
    bureau.add(enhanced_travel_planning.photo_spots_agent)
    bureau.add(enhanced_travel_planning.dietary_agent)
    bureau.add(enhanced_travel_planning.transportation_agent)
    bureau.add(enhanced_travel_planning.events_agent)
    
    print("\n=== ZenJourney Multi-Agent Travel Planning System ===\n")
    print("Starting all agents. The travel planning API will be available at:")
    print("https://zenjourney.onrender.com/travel/plan\n")
    print("You can also directly test the API with a curl command:")
    print("""curl -d '{"destination":"Paris, France", "start_date":"2023-08-01", "end_date":"2023-08-07", "budget":2000.0, "preferences":"vegetarian, museums, photography"}' -H "Content-Type: application/json" -X POST https://zenjourney.onrender.com""")
    print("\nPress Ctrl+C to stop all agents")
    
    # Run the bureau
    bureau.run() 