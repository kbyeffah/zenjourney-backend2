#!/usr/bin/env python3
from uagents import Agent, Context, Model

class TransportationRequest(Model):
    destination: str
    duration_days: int

class TransportationResponse(Model):
    recommendations: str
    estimated_cost: float

# Create the transportation agent
transportation_agent = Agent(
    name="transportation_advisor",
    port=8006,
    endpoint=["http://localhost:8006/submit"],
)

@transportation_agent.on_event("startup")
async def startup(ctx: Context):
    ctx.logger.info(f"Transportation Advisor Agent started with address: {transportation_agent.address}")

@transportation_agent.on_message(model=TransportationRequest)
async def handle_transportation_request(ctx: Context, sender: str, msg: TransportationRequest):
    ctx.logger.info(f"Received transportation request for {msg.destination} for {msg.duration_days} days")
    
    # Get transportation recommendations
    recommendations, estimated_cost = get_transportation_info(msg.destination, msg.duration_days)
    
    # Create and send the response
    response = TransportationResponse(
        recommendations=recommendations,
        estimated_cost=estimated_cost
    )
    await ctx.send(sender, response)

def get_transportation_info(destination, duration_days):
    """Get transportation recommendations and cost estimates."""
    destination = destination.lower()
    
    # Default transportation recommendations
    recommendations = f"TRANSPORTATION OPTIONS IN {destination.upper()}:\n\n"
    estimated_cost = 50.0 * duration_days  # Default estimate
    
    # Customize based on popular destinations
    if "paris" in destination:
        recommendations += """
GETTING AROUND PARIS:

PUBLIC TRANSPORTATION:
- Paris Metro: Extensive subway system covering all major attractions
- RER Trains: Connect city center with suburbs, airports, and Versailles
- Buses: Complement the Metro network with scenic routes
- Trams: Primarily serve the city perimeter

RECOMMENDED PASSES:
- Paris Visite Pass: 1, 2, 3, or 5 consecutive days of unlimited travel
- Navigo Découverte: Weekly pass (Monday-Sunday), best for 5+ day stays
- Mobilis: One-day unlimited travel pass

ALTERNATIVE OPTIONS:
- Vélib' Bike Share: Extensive network of rental bikes (€5/day or €20/week)
- Walking: Central Paris is compact and walkable between many attractions
- Taxis/Uber: Available but expensive compared to public transit
- Electric scooters: Several rental companies available via apps

AIRPORT TRANSFERS:
- From Charles de Gaulle: RER B train (€11.40, 30-45 min) or Airport Bus (€12.50)
- From Orly: Orlybus (€9.50, 30-40 min) or Orlyval + RER B (€12.10)

TIPS:
- Metro lines are numbered 1-14 with color coding
- Last Metro trains run around 1:15 AM (Fri/Sat) and 12:45 AM (other days)
- Keep your ticket until you exit the system to avoid fines
- Buses require validation upon boarding
"""
        estimated_cost = 10.0 * duration_days  # €10 per day average for public transport
    
    elif "tokyo" in destination:
        recommendations += """
GETTING AROUND TOKYO:

PUBLIC TRANSPORTATION:
- Tokyo Metro and Toei Subway: Extensive network covering most tourist areas
- JR Trains: Including the Yamanote Line that loops around central Tokyo
- Buses: Useful for areas not covered by trains
- Streetcars: Toden Arakawa Line offers a nostalgic ride

RECOMMENDED PASSES:
- Suica or PASMO IC Card: Rechargeable smart card for all transportation (¥500 deposit)
- Tokyo Subway Ticket: 24, 48, or 72-hour unlimited subway rides (tourists only)
- Tokyo Metro 24-hour Ticket: Unlimited Tokyo Metro lines for 24 hours
- JR Pass: For travelers planning side trips outside Tokyo

ALTERNATIVE OPTIONS:
- Taxis: Convenient but expensive, starting at ¥410-730 depending on time
- Rental bicycles: Available in some areas, but be aware of regulations
- Walking: Effective in specific neighborhoods, but Tokyo is vast

AIRPORT TRANSFERS:
- From Narita: Narita Express (¥3,070, 60 min), Skyliner (¥2,520, 40 min), or Airport Limousine Bus (¥3,100)
- From Haneda: Tokyo Monorail (¥500, 15 min) or Keikyu Line (¥300, 20 min)

TIPS:
- Trains stop running around midnight until 5 AM
- Rush hours (7:30-9:30 AM, 5:30-7:30 PM) are extremely crowded
- Station signs and announcements are in English
- Google Maps works excellently for navigation in Japan
"""
        estimated_cost = 15.0 * duration_days  # ¥1500 (approx $15) per day average
    
    elif "new york" in destination:
        recommendations += """
GETTING AROUND NEW YORK CITY:

PUBLIC TRANSPORTATION:
- Subway: Extensive 24/7 system with 472 stations across 5 boroughs
- Buses: Comprehensive network, good for crosstown travel
- Staten Island Ferry: Free service with great views of the Statue of Liberty

RECOMMENDED PASSES:
- MetroCard: $33 for 7-day unlimited rides on subways and buses
- OMNY: Contactless payment system accepting credit cards and mobile wallets
- Express Bus MetroCard: For longer commutes including express buses

ALTERNATIVE OPTIONS:
- Taxis/Uber/Lyft: Widely available but can be expensive in traffic
- Citi Bike: Bike sharing program ($12/day or $24/3-days)
- NYC Ferry: $4 per ride connecting waterfront neighborhoods
- Walking: Manhattan's grid system makes navigation easy

AIRPORT TRANSFERS:
- From JFK: AirTrain + Subway ($8.75, 60-90 min) or taxi (flat rate $52 plus tolls)
- From LaGuardia: Q70 SBS bus to subway (MetroCard fare) or taxi ($30-40)
- From Newark: AirTrain + NJ Transit ($15.25, 45 min) or taxi ($50-70)

TIPS:
- Subway runs 24/7 but service changes often occur on nights/weekends
- Express trains (marked with diamond symbol) skip local stops
- Use MTA Trip Planner or Google Maps for route planning
- Stand clear of the closing doors!
"""
        estimated_cost = 12.0 * duration_days  # $12 per day average
    
    elif "london" in destination:
        recommendations += """
GETTING AROUND LONDON:

PUBLIC TRANSPORTATION:
- London Underground (Tube): Extensive subway system with 11 lines
- Buses: Comprehensive network with over 700 routes
- London Overground and TfL Rail: Suburban train services
- DLR (Docklands Light Railway): Serves East London
- Trams: Operating in South London

RECOMMENDED PASSES:
- Oyster Card: Reloadable smart card with daily caps (£5 deposit)
- Contactless Payment Cards: Same fares as Oyster without deposit
- Travelcards: 1-day, 7-day, or monthly unlimited travel passes
- Visitor Oyster Card: Pre-loaded card with special offers

ALTERNATIVE OPTIONS:
- Santander Cycles: Bike sharing scheme (£2 access fee, then free for rides under 30 min)
- Black Cabs: Iconic but expensive, no need to pre-book
- Uber/Bolt: Widely available ride-sharing services
- River Bus Services: Thames Clipper boats along the river

AIRPORT TRANSFERS:
- From Heathrow: Tube (£5.50, 60 min), Heathrow Express (£25, 15 min), or TfL Rail (£11.60, 30 min)
- From Gatwick: Gatwick Express (£19.90, 30 min) or Thameslink (£11, 45 min)
- From Stansted: Stansted Express (£19, 45 min)
- From Luton: Thameslink + shuttle bus (£15.70, 60 min)

TIPS:
- Travel outside peak hours (6:30-9:30 AM, 4-7 PM) for cheaper fares
- Night Tube runs on Fri/Sat nights on select lines
- Night buses operate when the Tube is closed
- Download the TfL Go app for real-time information
"""
        estimated_cost = 15.0 * duration_days  # £15 per day average
    
    elif "bali" in destination:
        recommendations += """
GETTING AROUND BALI:

TRANSPORTATION OPTIONS:
- Private Driver: Most convenient option, typically $40-50 per day for 8-10 hours
- Scooter/Motorbike Rental: Most affordable option (60,000-100,000 IDR/day, $4-7)
- Taxis: Metered Blue Bird taxis are reliable in southern Bali
- Ride-Hailing Apps: Grab and Gojek offer car and motorbike rides
- Shuttle Services: Connect major tourist areas (Kuta, Ubud, etc.)

PUBLIC TRANSPORTATION:
- Bemos (Minivans): Local public transport, mostly used by residents
- Public Buses: Limited routes, not commonly used by tourists
- Perama Shuttle: Tourist shuttle between major destinations

AIRPORT TRANSFERS:
- Airport Taxi: Fixed price counters at airport (150,000-300,000 IDR, $10-20)
- Pre-arranged Hotel Transfer: Usually comparable to taxi rates
- Ride-Hailing Apps: Pickup point is located away from main terminal

AREA-SPECIFIC ADVICE:
- Ubud: Walkable center, but you'll need transport for outlying attractions
- Kuta/Seminyak/Canggu: Walkable beaches and centers, but distances between areas require transport
- Uluwatu: Spread out, requires vehicle to get between beaches and attractions
- Nusa Islands: Small enough to explore by motorbike or bicycle

TIPS:
- Renting a scooter requires an international driving permit
- Traffic can be chaotic - inexperienced riders should avoid scooters
- Negotiate and agree on prices before getting in unmarked taxis
- For day trips to multiple attractions, hiring a driver is most efficient
- Download Grab and Gojek apps before arriving
"""
        estimated_cost = 25.0 * duration_days  # $25 per day average (more if private driver)
    
    else:
        # Generic recommendations
        recommendations += """
GENERAL TRANSPORTATION ADVICE:

PUBLIC TRANSPORTATION:
- Research the public transportation options before arriving
- Look for tourist travel cards that offer unlimited rides
- Download the local transport app if available
- Consider the balance between cost and convenience

ALTERNATIVE OPTIONS:
- Ride-sharing apps: Check if Uber, Lyft, or local alternatives operate
- Taxis: Know the reputable companies and typical fares
- Rental cars: Best for destinations with limited public transport
- Bike rentals: Good option in bike-friendly cities

MONEY-SAVING TIPS:
- Stay in a central location to minimize transportation needs
- Look for day passes or multi-day transportation passes
- Group attractions by area to minimize travel between them
- Consider walking for destinations under 30 minutes away

SAFETY TIPS:
- Research common transportation scams for your destination
- Keep valuables secure, especially in crowded vehicles
- Have a paper map as backup for technology failures
- Save your accommodation address in the local language
"""
        estimated_cost = 20.0 * duration_days  # Generic estimate
    
    return recommendations, estimated_cost

if __name__ == "__main__":
    transportation_agent.run() 