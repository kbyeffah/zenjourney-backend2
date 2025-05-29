import os
from dotenv import load_dotenv
from datetime import datetime, timedelta
import json
import fetchai
from uagents import Agent, Context

# Load environment variables
load_dotenv()

class FetchAIAgent:
    def __init__(self):
        self.api_key = os.getenv('FETCH_AI_API_KEY')
        if not self.api_key:
            raise ValueError("FETCH_AI_API_KEY not found in environment variables")
        
        # Initialize Fetch AI agent
        self.agent = Agent(
            name="fetch_ai_agent",
            port=8008,
            endpoint=["http://localhost:8008/submit"],
        )
        
    async def create_calendar_event(self, title, start_time, end_time, description=""):
        """
        Create a calendar event using Fetch AI
        """
        try:
            # Create event data
            event_data = {
                "title": title,
                "start_time": start_time.isoformat(),
                "end_time": end_time.isoformat(),
                "description": description
            }
            
            # Use Fetch AI to create event
            await self.agent.context.send(
                self.agent.address,
                {"type": "create_event", "data": event_data}
            )
            
            return {"status": "success", "message": "Event created successfully", "data": event_data}
            
        except Exception as e:
            return {"status": "error", "message": str(e)}
    
    async def get_calendar_events(self, start_date, end_date):
        """
        Retrieve calendar events for a specific date range
        """
        try:
            # Query events
            events = []  # This would be replaced with actual event fetching
            return {"status": "success", "events": events}
            
        except Exception as e:
            return {"status": "error", "message": str(e)}
    
    async def create_agentic_workflow(self, workflow_name, steps):
        """
        Create an agentic workflow using Fetch AI
        """
        try:
            workflow_data = {
                "name": workflow_name,
                "steps": steps,
                "created_at": datetime.now().isoformat()
            }
            
            # Use Fetch AI to create workflow
            await self.agent.context.send(
                self.agent.address,
                {"type": "create_workflow", "data": workflow_data}
            )
            
            return {"status": "success", "message": "Workflow created successfully", "workflow_id": "sample_id"}
            
        except Exception as e:
            return {"status": "error", "message": str(e)}
    
    async def execute_workflow(self, workflow_id):
        """
        Execute a specific workflow
        """
        try:
            # Use Fetch AI to execute workflow
            await self.agent.context.send(
                self.agent.address,
                {"type": "execute_workflow", "workflow_id": workflow_id}
            )
            
            return {"status": "success", "message": "Workflow executed successfully"}
            
        except Exception as e:
            return {"status": "error", "message": str(e)} 