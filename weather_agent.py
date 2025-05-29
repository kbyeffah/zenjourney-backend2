from uagents import Agent, Context, Model

class WeatherRequest(Model):
    destination: str
    start_date: str
    end_date: str

class WeatherResponse(Model):
    destination: str
    forecast: str
    avg_temp: float
    clothing_suggestions: str

# Create the weather agent
weather_agent = Agent(
    name="weather_advisor",
    port=8002,
    endpoint=["http://localhost:8002/submit"],
)

@weather_agent.on_event("startup")
async def startup(ctx: Context):
    ctx.logger.info(f"Weather Advisor Agent started with address: {weather_agent.address}")

@weather_agent.on_message(model=WeatherRequest)
async def handle_weather_request(ctx: Context, sender: str, msg: WeatherRequest):
    ctx.logger.info(f"Received weather request for {msg.destination} from {sender}")
    
    # In a real implementation, you would call a weather API here
    # For this example, we're simulating responses based on the destination
    
    # Simple weather simulation based on destination
    weather_data = get_simulated_weather(msg.destination, msg.start_date, msg.end_date)
    
    # Create and send the response
    response = WeatherResponse(
        destination=msg.destination,
        forecast=weather_data["forecast"],
        avg_temp=weather_data["avg_temp"],
        clothing_suggestions=weather_data["clothing_suggestions"]
    )
    
    await ctx.send(sender, response)

def get_simulated_weather(destination, start_date, end_date):
    """Simulate weather data for a given destination."""
    destination = destination.lower()
    
    # Default weather data
    weather_data = {
        "forecast": "Partly cloudy with occasional showers.",
        "avg_temp": 22.0,
        "clothing_suggestions": "Light to medium layers, bring a light jacket and umbrella."
    }
    
    # Customize based on popular destinations
    if "paris" in destination:
        weather_data = {
            "forecast": "Mild temperatures with occasional rain. Partly cloudy most days.",
            "avg_temp": 18.5,
            "clothing_suggestions": "Light layers, a stylish jacket, comfortable walking shoes, and a compact umbrella."
        }
    elif "tokyo" in destination:
        weather_data = {
            "forecast": "Warm and humid with potential afternoon showers.",
            "avg_temp": 24.0,
            "clothing_suggestions": "Light, breathable clothing, comfortable walking shoes, and a small umbrella."
        }
    elif "new york" in destination:
        weather_data = {
            "forecast": "Variable weather with potential for rain or sunshine. Cooler evenings.",
            "avg_temp": 20.0,
            "clothing_suggestions": "Layers including light sweaters, a versatile jacket, and comfortable walking shoes."
        }
    elif "bali" in destination:
        weather_data = {
            "forecast": "Hot and humid with occasional tropical showers. Very sunny.",
            "avg_temp": 29.5,
            "clothing_suggestions": "Light, breathable clothing, sun protection (hat, sunglasses, sunscreen), sandals, and swimwear."
        }
    elif "london" in destination:
        weather_data = {
            "forecast": "Cool with frequent light rain and overcast skies.",
            "avg_temp": 16.0,
            "clothing_suggestions": "Layers, a waterproof jacket, umbrella, and comfortable waterproof shoes."
        }
    elif "sydney" in destination:
        weather_data = {
            "forecast": "Warm and sunny with mild evenings.",
            "avg_temp": 23.0,
            "clothing_suggestions": "Light clothing, sun protection, and a light layer for evenings."
        }
    elif "dubai" in destination:
        weather_data = {
            "forecast": "Very hot and dry with clear skies.",
            "avg_temp": 35.0,
            "clothing_suggestions": "Very light, loose clothing that covers skin for sun protection, hat, sunglasses, and sunscreen."
        }
    elif "rome" in destination:
        weather_data = {
            "forecast": "Warm and sunny with mild evenings.",
            "avg_temp": 25.0,
            "clothing_suggestions": "Light clothing, comfortable walking shoes, sun hat, and light layers for evening."
        }
    
    return weather_data

if __name__ == "__main__":
    weather_agent.run() 