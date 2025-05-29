#!/usr/bin/env python3
from uagents import Agent, Context, Model

class PhotoSpotsRequest(Model):
    destination: str

class PhotoSpotsResponse(Model):
    spots: str

# Create the photo spots agent
photo_spots_agent = Agent(
    name="photo_spots_finder",
    port=8004,
    endpoint=["http://localhost:8004/submit"],
)

@photo_spots_agent.on_event("startup")
async def startup(ctx: Context):
    ctx.logger.info(f"Photo Spots Finder Agent started with address: {photo_spots_agent.address}")

@photo_spots_agent.on_message(model=PhotoSpotsRequest)
async def handle_photo_spots_request(ctx: Context, sender: str, msg: PhotoSpotsRequest):
    ctx.logger.info(f"Received photo spots request for {msg.destination}")
    
    # Get photo spots for the destination
    photo_spots = get_photo_spots(msg.destination)
    
    # Create and send the response
    response = PhotoSpotsResponse(spots=photo_spots)
    await ctx.send(sender, response)

def get_photo_spots(destination):
    """Get photo spots for a given destination."""
    destination = destination.lower()
    
    # Default photo spots text
    photo_spots = "Popular viewpoints and landmarks make great photo opportunities."
    
    # Customize based on popular destinations
    if "paris" in destination:
        photo_spots = """
TOP PHOTO SPOTS IN PARIS:

1. Eiffel Tower (Trocadéro viewpoint) - Best at sunrise for fewer crowds
2. Louvre Museum Pyramid - Visit at night for dramatic lighting
3. Seine River Bridges - Pont Alexandre III is especially photogenic
4. Montmartre & Sacré-Cœur - Great city views from the steps
5. Notre-Dame Cathedral - Capture from Square Jean XXIII for the best angle
6. Luxembourg Gardens - Beautiful in spring and summer
7. Palais Royal Columns - Artistic black and white striped columns
8. Rue Crémieux - Colorful street with painted houses
9. Arc de Triomphe - Climb to the top for panoramic views
10. Galeries Lafayette rooftop - Free access with great city views

PHOTOGRAPHY TIPS:
- Early morning (6-8 AM) offers the best light and fewest tourists
- Blue hour (just after sunset) creates magical Parisian scenes
- Paris Museum Pass holders can skip lines at many attractions
"""
    elif "tokyo" in destination:
        photo_spots = """
TOP PHOTO SPOTS IN TOKYO:

1. Shibuya Crossing - Best from Starbucks or Mag's Park observation deck
2. Tokyo Skytree - For panoramic city views
3. Sensō-ji Temple in Asakusa - Most photogenic early morning
4. Meiji Shrine and its forested path
5. Shinjuku Gyoen National Garden - Especially during cherry blossom season
6. Harajuku's Takeshita Street - Vibrant youth culture and fashion
7. Nezu Shrine - Less crowded with beautiful torii gates
8. Tokyo Tower - Classic landmark especially beautiful at night
9. Chidorigafuchi Park - Stunning during cherry blossom season
10. teamLab Borderless Digital Art Museum - Incredible interactive art installations

PHOTOGRAPHY TIPS:
- Tokyo is very bright at night - great for night photography
- Rainy days create beautiful reflections on city streets
- Consider a telephoto lens to capture architectural details
"""
    elif "new york" in destination:
        photo_spots = """
TOP PHOTO SPOTS IN NEW YORK:

1. Brooklyn Bridge Park - Manhattan skyline view
2. Top of the Rock - Best NYC skyline view (better than Empire State Building)
3. Central Park - The Mall, Bow Bridge, and Bethesda Terrace
4. Grand Central Terminal - Iconic main concourse
5. DUMBO - Washington Street with Manhattan Bridge view
6. The Vessel at Hudson Yards - Unique honeycomb structure
7. The High Line - Elevated park with urban views
8. Times Square - Vibrant at night with neon lights
9. Flatiron Building - Best angle from 5th Ave and 23rd Street
10. One World Observatory - Highest viewpoint in NYC

PHOTOGRAPHY TIPS:
- Blue hour (just after sunset) is magical for skyline photos
- Use the NYC Ferry for unique perspectives from the water
- Weekday mornings are best for fewer crowds in popular spots
"""
    elif "bali" in destination:
        photo_spots = """
TOP PHOTO SPOTS IN BALI:

1. Tegallalang Rice Terraces - Best in early morning light
2. Uluwatu Temple - Dramatic clifftop temple, especially at sunset
3. Kelingking Beach (Nusa Penida) - The famous T-Rex shaped cliff
4. Lempuyang Temple (Gates of Heaven) - Frame Mount Agung through the gates
5. Handara Gate - Iconic Balinese gateway
6. Tibumana Waterfall - Less crowded than other waterfalls
7. Campuhan Ridge Walk - Beautiful morning walk in Ubud
8. Tukad Cepung Waterfall - Unique light beams through cave opening
9. Pura Ulun Danu Bratan - Iconic lakeside temple
10. Bali Swing in Ubud - For adventurous photos

PHOTOGRAPHY TIPS:
- Visit temple sites early morning (before 9 AM) to avoid crowds
- The "golden hour" light in Bali is exceptional for portraits
- Bring a polarizing filter for waterfalls and ocean scenes
- Respect local customs when photographing temples
"""
    elif "rome" in destination:
        photo_spots = """
TOP PHOTO SPOTS IN ROME:

1. Roman Colosseum - Best from Parco del Colle Oppio at sunrise
2. St. Peter's Square and Basilica - Early morning for fewer crowds
3. Trevi Fountain - Try to visit before 7 AM or after 11 PM
4. Spanish Steps - Beautiful with spring flowers
5. Ponte Sant'Angelo - Angel statues with St. Peter's in background
6. The Orange Garden (Giardino degli Aranci) - Panoramic city view
7. Roman Forum - Historic ruins best photographed in golden hour
8. Villa Borghese Gardens - Lush greenery and architecture
9. Pantheon - Amazing interior light beam
10. Pincio Terrace - Sunset view over Piazza del Popolo

PHOTOGRAPHY TIPS:
- Early morning (6-8 AM) offers the best light and empty streets
- Consider a tripod for night shots of monuments
- Look for reflections in puddles after rain
"""
    
    return photo_spots

if __name__ == "__main__":
    photo_spots_agent.run() 