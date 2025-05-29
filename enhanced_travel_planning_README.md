# ZenJourney - Enhanced Multi-Agent Travel Planning System

This project implements a comprehensive travel planning system using the uAgents framework from Fetch.ai. It demonstrates how multiple specialized agents can work together synchronously to create a detailed travel plan.

## System Architecture

The system consists of the following specialized agents:

1. **Travel Planning Agent** - The main coordinator that receives travel requests from users and communicates with specialized agents to create a comprehensive travel plan
2. **Weather Advisor Agent** - Provides weather forecasts and clothing/packing suggestions based on the destination and travel dates
3. **Budget Planner Agent** - Offers a detailed budget breakdown, optimizing how to allocate travel funds
4. **Photo Spots Finder Agent** - Recommends the best photography locations at the destination
5. **Dietary Planner Agent** - Gives food recommendations based on destination and dietary preferences
6. **Transportation Advisor Agent** - Provides transportation options with cost estimates
7. **Events Finder Agent** - Finds local events happening during the travel dates

## Agent Communication Pattern

The system uses the `send_and_receive` method from the uAgents framework to implement a synchronous request-response pattern. This allows the main Travel Planning Agent to wait for responses from specialized agents before compiling the final travel plan.

## Installation

1. Create a virtual environment and activate it:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```

## Running the System

You can run all agents together using the Bureau:

```bash
python run_all_agents.py
```

Alternatively, you can run each agent in a separate terminal:

```bash
# Terminal 1 (Main Travel Planning Agent)
python enhanced_travel_planning.py

# Terminal 2 (Weather Advisor Agent)
python weather_agent.py

# Terminal 3 (Budget Planner Agent)
python budget_agent.py

# Terminal 4 (Photo Spots Finder Agent)
python photo_spots_agent.py

# Terminal 5 (Dietary Planner Agent)
python dietary_agent.py

# Terminal 6 (Transportation Advisor Agent)
python transportation_agent.py

# Terminal 7 (Events Finder Agent)
python events_agent.py
```

## API Access

The Travel Planning Agent exposes a REST API endpoint at:
`http://localhost:8001/travel/plan`

You can use curl to send requests:

```bash
curl -d '{"destination":"Paris, France", "start_date":"2023-08-01", "end_date":"2023-08-07", "budget":2000.0, "preferences":"vegetarian, museums, photography"}' -H "Content-Type: application/json" -X POST http://localhost:8001/travel/plan
```

## Features

- **Synchronous Agent Communication**: Agents wait for responses from other agents using the `send_and_receive` method
- **REST API Integration**: Frontend can communicate with the agent system via REST API
- **Specialized Agents**: Each agent focuses on a specific aspect of travel planning
- **Customized Recommendations**: All recommendations are tailored to the specific destination and user preferences

## Example Travel Plan

The system generates a comprehensive travel plan that includes:

- Weather forecast and packing suggestions
- Budget breakdown with daily allocations
- Must-visit photo spots with photography tips
- Food recommendations based on dietary preferences
- Transportation options with cost estimates
- Local events happening during the stay
- A daily itinerary framework

## Frontend Integration

The travel planning agents connect to the ZenJourney frontend, which provides a user-friendly interface for submitting travel requests and viewing the generated travel plans.

## Based On

This project follows the uAgent to uAgent communication patterns described in the [fetch.ai documentation](https://innovationlab.fetch.ai/resources/docs/agent-communication/uagent-uagent-communication), particularly utilizing the synchronous `send_and_receive` method for coordinated agent responses. 