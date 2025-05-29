from uagents import Agent, Bureau, Context, Model
from datetime import datetime
import json


class VacationRequest(Model):
    destination: str
    start_date: str
    end_date: str
    budget: float
    preferences: str


class FlightInfo(Model):
    airline: str
    flight_number: str
    departure_time: str
    arrival_time: str
    price: float


class HotelInfo(Model):
    name: str
    address: str
    check_in: str
    check_out: str
    price_per_night: float
    total_price: float


class ActivitiesInfo(Model):
    activities: list
    total_price: float


class VacationPackage(Model):
    destination: str
    flight: FlightInfo
    hotel: HotelInfo
    activities: ActivitiesInfo
    total_cost: float


# Create agents for different services
user_agent = Agent(name="user", seed="user seed phrase", port=8010)
travel_agent = Agent(name="travel_agent", seed="travel agent seed phrase", port=8011)
flight_agent = Agent(name="flight_agent", seed="flight agent seed phrase", port=8012)
hotel_agent = Agent(name="hotel_agent", seed="hotel agent seed phrase", port=8013)
activities_agent = Agent(name="activities_agent", seed="activities agent seed phrase", port=8014)


# Simulated flight database
FLIGHT_DB = {
    "Tokyo": [
        {"airline": "JAL", "flight_number": "JL001", "departure_time": "08:00", "arrival_time": "22:00", "price": 1200.0},
        {"airline": "ANA", "flight_number": "NH002", "departure_time": "10:30", "arrival_time": "00:30", "price": 1150.0}
    ],
    "Paris": [
        {"airline": "Air France", "flight_number": "AF001", "departure_time": "09:15", "arrival_time": "15:45", "price": 950.0},
        {"airline": "Delta", "flight_number": "DL032", "departure_time": "12:00", "arrival_time": "18:30", "price": 1000.0}
    ],
    "Rome": [
        {"airline": "Alitalia", "flight_number": "AZ123", "departure_time": "07:30", "arrival_time": "13:45", "price": 890.0},
        {"airline": "Lufthansa", "flight_number": "LH456", "departure_time": "14:20", "arrival_time": "20:35", "price": 920.0}
    ]
}

# Simulated hotel database
HOTEL_DB = {
    "Tokyo": [
        {"name": "Imperial Hotel", "address": "1-1-1 Uchisaiwaicho, Tokyo", "price_per_night": 250.0},
        {"name": "Park Hyatt Tokyo", "address": "3-7-1-2 Nishi Shinjuku, Tokyo", "price_per_night": 350.0}
    ],
    "Paris": [
        {"name": "Hotel de Crillon", "address": "10 Place de la Concorde, Paris", "price_per_night": 400.0},
        {"name": "Le Meurice", "address": "228 Rue de Rivoli, Paris", "price_per_night": 450.0}
    ],
    "Rome": [
        {"name": "Hotel Hassler", "address": "Piazza Trinità dei Monti 6, Rome", "price_per_night": 300.0},
        {"name": "Hotel de Russie", "address": "Via del Babuino 9, Rome", "price_per_night": 350.0}
    ]
}

# Simulated activities database
ACTIVITIES_DB = {
    "Tokyo": [
        {"name": "Tokyo Skytree Visit", "price": 25.0},
        {"name": "Tsukiji Fish Market Tour", "price": 75.0},
        {"name": "Sumo Wrestling Match", "price": 100.0},
        {"name": "Mt. Fuji Day Trip", "price": 150.0},
        {"name": "Robot Restaurant Show", "price": 80.0}
    ],
    "Paris": [
        {"name": "Eiffel Tower Skip-the-Line", "price": 60.0},
        {"name": "Louvre Museum Guided Tour", "price": 65.0},
        {"name": "Seine River Cruise", "price": 35.0},
        {"name": "Montmartre Walking Tour", "price": 25.0},
        {"name": "Versailles Palace Day Trip", "price": 90.0}
    ],
    "Rome": [
        {"name": "Colosseum & Roman Forum Tour", "price": 55.0},
        {"name": "Vatican Museums & Sistine Chapel", "price": 70.0},
        {"name": "Pasta Making Class", "price": 85.0},
        {"name": "Trastevere Food Tour", "price": 95.0},
        {"name": "Pompeii Day Trip", "price": 150.0}
    ]
}


@user_agent.on_interval(period=10.0)
async def request_vacation(ctx: Context):
    # Only send one request
    if hasattr(ctx.storage, "request_sent") and ctx.storage.request_sent:
        return
    
    vacation_request = VacationRequest(
        destination="Tokyo",
        start_date="2023-07-15",
        end_date="2023-07-22",
        budget=3000.0,
        preferences="Cultural experiences, good food, technology"
    )
    
    ctx.logger.info(f"User is requesting a vacation package to {vacation_request.destination}")
    
    reply, status = await ctx.send_and_receive(
        travel_agent.address, 
        vacation_request, 
        response_type=VacationPackage
    )
    
    if isinstance(reply, VacationPackage):
        ctx.storage.request_sent = True
        ctx.logger.info(f"Received vacation package for {reply.destination}:")
        ctx.logger.info(f"Flight: {reply.flight.airline} {reply.flight.flight_number}")
        ctx.logger.info(f"Hotel: {reply.hotel.name}")
        ctx.logger.info(f"Activities: {json.dumps([a for a in reply.activities.activities], indent=2)}")
        ctx.logger.info(f"Total cost: ${reply.total_cost:.2f}")
    else:
        ctx.logger.error(f"Failed to receive vacation package: {status}")


@travel_agent.on_message(model=VacationRequest)
async def handle_vacation_request(ctx: Context, sender: str, msg: VacationRequest):
    ctx.logger.info(f"Travel agent received vacation request for {msg.destination}")
    
    # 1. Request flight information
    ctx.logger.info("Travel agent is requesting flight information")
    flight_reply, flight_status = await ctx.send_and_receive(
        flight_agent.address,
        msg,
        response_type=FlightInfo
    )
    
    if not isinstance(flight_reply, FlightInfo):
        ctx.logger.error(f"Failed to get flight information: {flight_status}")
        return
    
    ctx.logger.info(f"Travel agent received flight information for {flight_reply.airline} {flight_reply.flight_number}")
    
    # 2. Request hotel information
    ctx.logger.info("Travel agent is requesting hotel information")
    hotel_reply, hotel_status = await ctx.send_and_receive(
        hotel_agent.address,
        msg,
        response_type=HotelInfo
    )
    
    if not isinstance(hotel_reply, HotelInfo):
        ctx.logger.error(f"Failed to get hotel information: {hotel_status}")
        return
    
    ctx.logger.info(f"Travel agent received hotel information for {hotel_reply.name}")
    
    # 3. Request activities information
    ctx.logger.info("Travel agent is requesting activities information")
    activities_reply, activities_status = await ctx.send_and_receive(
        activities_agent.address,
        msg,
        response_type=ActivitiesInfo
    )
    
    if not isinstance(activities_reply, ActivitiesInfo):
        ctx.logger.error(f"Failed to get activities information: {activities_status}")
        return
    
    ctx.logger.info(f"Travel agent received activities information with {len(activities_reply.activities)} activities")
    
    # 4. Calculate total cost and create vacation package
    total_cost = flight_reply.price + hotel_reply.total_price + activities_reply.total_price
    
    vacation_package = VacationPackage(
        destination=msg.destination,
        flight=flight_reply,
        hotel=hotel_reply,
        activities=activities_reply,
        total_cost=total_cost
    )
    
    # 5. Send vacation package back to the user
    ctx.logger.info(f"Travel agent is sending complete vacation package to user (total: ${total_cost:.2f})")
    await ctx.send(sender, vacation_package)


@flight_agent.on_message(model=VacationRequest)
async def handle_flight_request(ctx: Context, sender: str, msg: VacationRequest):
    ctx.logger.info(f"Flight agent received request for flights to {msg.destination}")
    
    # Find available flights for the destination
    available_flights = FLIGHT_DB.get(msg.destination, [])
    
    if not available_flights:
        ctx.logger.error(f"No flights found for {msg.destination}")
        return
    
    # Select the cheapest flight
    cheapest_flight = min(available_flights, key=lambda x: x["price"])
    
    flight_info = FlightInfo(
        airline=cheapest_flight["airline"],
        flight_number=cheapest_flight["flight_number"],
        departure_time=cheapest_flight["departure_time"],
        arrival_time=cheapest_flight["arrival_time"],
        price=cheapest_flight["price"]
    )
    
    ctx.logger.info(f"Flight agent found flight: {flight_info.airline} {flight_info.flight_number} (${flight_info.price:.2f})")
    await ctx.send(sender, flight_info)


@hotel_agent.on_message(model=VacationRequest)
async def handle_hotel_request(ctx: Context, sender: str, msg: VacationRequest):
    ctx.logger.info(f"Hotel agent received request for hotels in {msg.destination}")
    
    # Find available hotels for the destination
    available_hotels = HOTEL_DB.get(msg.destination, [])
    
    if not available_hotels:
        ctx.logger.error(f"No hotels found for {msg.destination}")
        return
    
    # Select the cheapest hotel
    cheapest_hotel = min(available_hotels, key=lambda x: x["price_per_night"])
    
    # Calculate number of nights
    start_date = datetime.strptime(msg.start_date, "%Y-%m-%d")
    end_date = datetime.strptime(msg.end_date, "%Y-%m-%d")
    num_nights = (end_date - start_date).days
    
    total_price = cheapest_hotel["price_per_night"] * num_nights
    
    hotel_info = HotelInfo(
        name=cheapest_hotel["name"],
        address=cheapest_hotel["address"],
        check_in=msg.start_date,
        check_out=msg.end_date,
        price_per_night=cheapest_hotel["price_per_night"],
        total_price=total_price
    )
    
    ctx.logger.info(f"Hotel agent found hotel: {hotel_info.name} (${hotel_info.total_price:.2f} for {num_nights} nights)")
    await ctx.send(sender, hotel_info)


@activities_agent.on_message(model=VacationRequest)
async def handle_activities_request(ctx: Context, sender: str, msg: VacationRequest):
    ctx.logger.info(f"Activities agent received request for activities in {msg.destination}")
    
    # Find available activities for the destination
    available_activities = ACTIVITIES_DB.get(msg.destination, [])
    
    if not available_activities:
        ctx.logger.error(f"No activities found for {msg.destination}")
        return
    
    # Select activities based on budget and preferences
    preferences_keywords = [kw.strip().lower() for kw in msg.preferences.split(",")]
    selected_activities = []
    total_price = 0.0
    
    # Select up to 3 activities
    for activity in available_activities[:3]:
        selected_activities.append(activity)
        total_price += activity["price"]
    
    activities_info = ActivitiesInfo(
        activities=selected_activities,
        total_price=total_price
    )
    
    ctx.logger.info(f"Activities agent found {len(selected_activities)} activities (total: ${total_price:.2f})")
    await ctx.send(sender, activities_info)


# Add all agents to the bureau and set the bureau port
bureau = Bureau(agents=[user_agent, travel_agent, flight_agent, hotel_agent, activities_agent], port=8009)

if __name__ == "__main__":
    print("Starting Vacation Planning System with Synchronous Communication")
    print("This example demonstrates multiple agents working together to create a vacation package")
    print("Press Ctrl+C to exit")
    print("-" * 75)
    bureau.run() 