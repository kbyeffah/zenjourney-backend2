from uagents import Bureau
from travel_request_agent import request_agent
from travel_planning_agent import planning_agent

# Create the bureau to manage both agents
bureau = Bureau()

# Add both agents to the bureau
bureau.add(request_agent)
bureau.add(planning_agent)

# Update the planning agent address in the request agent
import travel_request_agent
travel_request_agent.planning_agent_address = planning_agent.address

if __name__ == "__main__":
    print("Starting Travel Planning System...")
    print(f"Request Agent Address: {request_agent.address}")
    print(f"Planning Agent Address: {planning_agent.address}")
    print("Use CTRL+C to exit")
    
    # Run the bureau to manage both agents
    bureau.run()