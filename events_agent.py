#!/usr/bin/env python3
from uagents import Agent, Context, Model
from datetime import datetime, timedelta

class EventsRequest(Model):
    destination: str
    start_date: str
    end_date: str

class EventsResponse(Model):
    events: str

# Create the events agent
events_agent = Agent(
    name="events_finder",
    port=8007,
    endpoint=["http://localhost:8007/submit"],
)

@events_agent.on_event("startup")
async def startup(ctx: Context):
    ctx.logger.info(f"Events Finder Agent started with address: {events_agent.address}")

@events_agent.on_message(model=EventsRequest)
async def handle_events_request(ctx: Context, sender: str, msg: EventsRequest):
    ctx.logger.info(f"Received events request for {msg.destination} from {msg.start_date} to {msg.end_date}")
    
    # Parse dates
    start_date = datetime.strptime(msg.start_date, "%Y-%m-%d")
    end_date = datetime.strptime(msg.end_date, "%Y-%m-%d")
    
    # Get events information
    events_info = get_events(msg.destination, start_date, end_date)
    
    # Create and send the response
    response = EventsResponse(events=events_info)
    await ctx.send(sender, response)

def get_events(destination, start_date, end_date):
    """Get events for a given destination and date range."""
    destination = destination.lower()
    
    # Determine month name for the start date
    month_name = start_date.strftime("%B")
    year = start_date.year
    
    # Default events info
    events_info = f"LOCAL EVENTS IN {destination.upper()} DURING YOUR STAY:\n\n"
    
    # Add note about simulation
    events_info += "Note: In an actual implementation, this would connect to event APIs for real-time events.\n\n"
    
    # Customize based on popular destinations and month
    if "paris" in destination:
        if month_name in ["April", "May", "June"]:
            events_info += f"""
SEASONAL HIGHLIGHTS ({month_name}):
- French Open Tennis Tournament (Late May-Early June)
- Paris Jazz Festival (June)
- Fête de la Musique (June 21) - Free music throughout the city
- Spring flower displays at Jardin des Tuileries and Luxembourg Gardens

RECURRING EVENTS:
- First Sunday of the month: Free admission to many museums
- Louvre late openings on Wednesdays and Fridays
- Marché aux Puces de Saint-Ouen (flea market) on weekends
- Seine River night cruises

EXHIBITIONS & SHOWS:
- Centre Pompidou contemporary art exhibitions
- Palais de Tokyo avant-garde installations
- Ongoing shows at Opéra Garnier and Opéra Bastille
- Moulin Rouge and Lido cabaret performances
"""
        elif month_name in ["July", "August", "September"]:
            events_info += f"""
SEASONAL HIGHLIGHTS ({month_name}):
- Bastille Day Celebrations (July 14)
- Paris Plages (July-August) - Seine riverside beaches
- Open-air cinema at Parc de la Villette (July-August)
- European Heritage Days (September) - Access to normally closed buildings

RECURRING EVENTS:
- First Sunday of the month: Free admission to many museums
- Outdoor concerts in Parc Floral (summer)
- Evening boat cruises on the Seine
- Rock en Seine music festival (late August)
- Fashion Week (late September)

EXHIBITIONS & SHOWS:
- Special summer exhibitions at major museums
- Outdoor photography displays along Champs Elysées
- Sound and light shows at various monuments
"""
        else:
            events_info += """
RECURRING EVENTS:
- First Sunday of the month: Free admission to many museums
- Louvre late openings on Wednesdays and Fridays
- Weekend markets throughout the city
- Evening performances at famous venues

EXHIBITIONS & SHOWS:
- Rotating exhibitions at Grand Palais and Petit Palais
- Contemporary art at Palais de Tokyo
- Opera and ballet performances
- Cabaret shows at Moulin Rouge and Lido
"""
    
    elif "tokyo" in destination:
        if month_name in ["March", "April", "May"]:
            events_info += f"""
SEASONAL HIGHLIGHTS ({month_name}):
- Cherry Blossom (Sakura) Season (Late March-Early April)
- Hanami parties in major parks
- Kanamara Matsuri Festival (April) in Kawasaki
- Sanja Matsuri in Asakusa (May)
- Golden Week holidays (Late April-Early May)

RECURRING EVENTS:
- Sumo tournaments (January, May, September)
- Farmers markets at United Nations University (weekends)
- Yoyogi Park events and performances (weekends)
- Comiket manga and anime convention (varies)

EXHIBITIONS & SHOWS:
- TeamLab Borderless digital art exhibition
- Rotating exhibits at Mori Art Museum
- Tokyo National Museum special collections
- Kabuki performances at Kabukiza Theatre
"""
        elif month_name in ["June", "July", "August"]:
            events_info += f"""
SEASONAL HIGHLIGHTS ({month_name}):
- Rainy season (June) with hydrangea blooms
- Sumidagawa Fireworks Festival (July)
- Tanabata Festival (July 7)
- Obon Festival (mid-August)
- Summer festivals (matsuri) throughout the city

RECURRING EVENTS:
- Sumo tournaments (May, September)
- Morning tuna auctions at Toyosu Market
- Weekend food festivals in Yoyogi Park
- Robot shows at Robot Restaurant

EXHIBITIONS & SHOWS:
- Summer illuminations at Tokyo Midtown
- Fuji Rock Festival (late July)
- Tokyo Jazz Festival (late August/early September)
- Summer sonic music festival (mid-August)
"""
        else:
            events_info += """
RECURRING EVENTS:
- Sumo tournaments (January, May, September)
- Farmers markets at United Nations University (weekends)
- Morning tuna auctions at Toyosu Market
- Akihabara electronic district special events

EXHIBITIONS & SHOWS:
- TeamLab Borderless/Planets digital art exhibitions
- Rotating exhibits at major museums
- J-Pop and K-Pop concerts
- Traditional theater performances
"""
    
    elif "new york" in destination:
        if month_name in ["April", "May", "June"]:
            events_info += f"""
SEASONAL HIGHLIGHTS ({month_name}):
- Tribeca Film Festival (April)
- Cherry Blossom Festival at Brooklyn Botanic Garden (April)
- Frieze Art Fair (May)
- Shakespeare in the Park (June-August)
- Pride March and Festival (June)
- Museum Mile Festival (June)

RECURRING EVENTS:
- Broadway shows (discount tickets at TKTS booths)
- Free summer concerts in Central Park
- Weekly food markets: Smorgasburg in Brooklyn (weekends)
- Highline art installations and walking tours
- Saturday Night Live tapings (seasonal)

EXHIBITIONS & SHOWS:
- Metropolitan Museum of Art special exhibitions
- Whitney Museum American art collections
- MoMA contemporary installations
- New museum shows opening regularly
"""
        elif month_name in ["July", "August", "September"]:
            events_info += f"""
SEASONAL HIGHLIGHTS ({month_name}):
- Macy's 4th of July Fireworks
- Restaurant Week (late July/early August)
- US Open Tennis (August-September)
- Summer concerts in Central Park
- Outdoor movies in Bryant Park (summer)
- San Gennaro Festival in Little Italy (September)
- Fashion Week (September)

RECURRING EVENTS:
- Broadway shows (discount tickets at TKTS booths)
- Free museum days (check specific museums)
- Governor's Island summer activities
- Staten Island Ferry (free views of Statue of Liberty)
- Weekend street fairs throughout Manhattan

EXHIBITIONS & SHOWS:
- Rotating exhibitions at major museums
- Rooftop bars and summer pop-ups
- Shakespeare in the Park performances
- Concerts at Madison Square Garden
"""
        elif month_name in ["October", "November", "December"]:
            events_info += f"""
SEASONAL HIGHLIGHTS ({month_name}):
- New York Film Festival (October)
- Village Halloween Parade (October 31)
- Macy's Thanksgiving Day Parade (November)
- Rockefeller Center Christmas Tree Lighting (early December)
- New Year's Eve in Times Square (December 31)
- Holiday markets at Bryant Park, Union Square, and Columbus Circle

RECURRING EVENTS:
- Broadway shows (discount tickets at TKTS booths)
- NFL football games (Jets/Giants, September-December)
- NBA basketball games (Knicks/Nets, October-April)
- NHL hockey games (Rangers/Islanders, October-April)

EXHIBITIONS & SHOWS:
- Fall/winter exhibitions at major museums
- Holiday window displays on Fifth Avenue
- Radio City Christmas Spectacular
- The Nutcracker at Lincoln Center
"""
        else:
            events_info += """
RECURRING EVENTS:
- Broadway shows (discount tickets at TKTS booths)
- Free museum days (check specific museums)
- Live TV show tapings (The Tonight Show, Late Show, etc.)
- NYC Restaurant Week (winter and summer)
- Weekly comedy shows

EXHIBITIONS & SHOWS:
- Major exhibitions at Metropolitan Museum of Art
- MoMA contemporary art displays
- Live music in Greenwich Village and Brooklyn
- Off-Broadway theatrical productions
"""
    
    else:
        # Generic events for any destination
        events_info += f"""
GENERAL EVENT SUGGESTIONS:

LOCAL RESOURCES:
- Check the official tourism website for {destination}
- Visit the local tourist information center upon arrival
- Look for free city magazines and event listings
- Ask your hotel concierge for current events

RECURRING EVENTS:
- Local markets (farmers markets, craft markets, night markets)
- Museum free days or extended hours
- Live music venues and performances
- Seasonal festivals and celebrations

DIGITAL RESOURCES:
- Eventbrite, Meetup, or Facebook Events for your destination
- TimeOut guides if available for your city
- TripAdvisor's "Events" section
- Local newspaper websites for event calendars

CULTURAL OPPORTUNITIES:
- Theater and performing arts productions
- Sporting events
- Gallery openings and art walks
- Food festivals and culinary events
"""
    
    return events_info

if __name__ == "__main__":
    events_agent.run() 