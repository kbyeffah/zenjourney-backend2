import requests
import json
import sys

def query_travel_api(destination, start_date, end_date, budget, preferences):
    """Send a request to the travel planning API and print the response"""
    
    url = "https://zenjourney.onrender.com/travel/plan"
    
    # Create request payload
    payload = {
        "destination": destination,
        "start_date": start_date,
        "end_date": end_date,
        "budget": float(budget),
        "preferences": preferences
    }
    
    try:
        # Send POST request to API
        response = requests.post(url, json=payload)
        
        # Check if request was successful
        if response.status_code == 200:
            # Parse JSON response
            data = response.json()
            
            # Print formatted response
            print("\n=== Travel Plan ===")
            print(f"Destination: {data['destination']}")
            print(f"Estimated Cost: ${data['estimated_cost']}")
            print("\nItinerary:")
            print(data['itinerary'])
        else:
            print(f"Error: Received status code {response.status_code}")
            print(response.text)
    
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        print("Make sure the travel planning agent is running.")

if __name__ == "__main__":
    if len(sys.argv) < 6:
        print("Usage: python rest_client.py <destination> <start_date> <end_date> <budget> <preferences>")
        print("Example: python rest_client.py \"Paris, France\" 2023-08-01 2023-08-07 2000 \"Art, history, cuisine\"")
        sys.exit(1)
    
    # Get command line arguments
    destination = sys.argv[1]
    start_date = sys.argv[2]
    end_date = sys.argv[3]
    budget = sys.argv[4]
    preferences = sys.argv[5]
    
    # Query the API
    query_travel_api(destination, start_date, end_date, budget, preferences) 