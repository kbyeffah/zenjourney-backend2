#!/usr/bin/env python3
from uagents import Agent, Context, Model

class DietaryRequest(Model):
    destination: str
    preferences: str

class DietaryResponse(Model):
    recommendations: str

# Create the dietary agent
dietary_agent = Agent(
    name="dietary_planner",
    port=8005,
    endpoint=["http://localhost:8005/submit"],
)

@dietary_agent.on_event("startup")
async def startup(ctx: Context):
    ctx.logger.info(f"Dietary Planner Agent started with address: {dietary_agent.address}")

@dietary_agent.on_message(model=DietaryRequest)
async def handle_dietary_request(ctx: Context, sender: str, msg: DietaryRequest):
    ctx.logger.info(f"Received dietary request for {msg.destination} with preferences: {msg.preferences}")
    
    # Process the dietary preferences
    dietary_preferences = process_preferences(msg.preferences)
    
    # Get food recommendations
    recommendations = get_food_recommendations(msg.destination, dietary_preferences)
    
    # Create and send the response
    response = DietaryResponse(recommendations=recommendations)
    await ctx.send(sender, response)

def process_preferences(preferences):
    """Process the dietary preferences string to identify key preferences."""
    preferences = preferences.lower()
    
    dietary_prefs = {
        "vegetarian": "vegetarian" in preferences,
        "vegan": "vegan" in preferences,
        "gluten_free": "gluten free" in preferences or "gluten-free" in preferences,
        "dairy_free": "dairy free" in preferences or "dairy-free" in preferences or "lactose" in preferences,
        "halal": "halal" in preferences,
        "kosher": "kosher" in preferences,
        "allergies": any(allergy in preferences for allergy in ["allergy", "allergic", "nuts", "seafood", "shellfish"]),
        "spicy": "spicy" in preferences,
        "local": "local" in preferences or "authentic" in preferences or "traditional" in preferences,
        "budget": "cheap" in preferences or "budget" in preferences or "inexpensive" in preferences,
        "fine_dining": "fine dining" in preferences or "upscale" in preferences or "fancy" in preferences,
        "street_food": "street food" in preferences or "street vendor" in preferences
    }
    
    return dietary_prefs

def get_food_recommendations(destination, preferences):
    """Get food recommendations based on destination and preferences."""
    destination = destination.lower()
    
    # Start with general recommendations
    recommendations = f"FOOD RECOMMENDATIONS FOR {destination.upper()}:\n\n"
    
    # Add dietary restriction notice if applicable
    restriction_notes = []
    if preferences["vegetarian"]:
        restriction_notes.append("Vegetarian options")
    if preferences["vegan"]:
        restriction_notes.append("Vegan options")
    if preferences["gluten_free"]:
        restriction_notes.append("Gluten-free options")
    if preferences["dairy_free"]:
        restriction_notes.append("Dairy-free options")
    if preferences["halal"]:
        restriction_notes.append("Halal options")
    if preferences["kosher"]:
        restriction_notes.append("Kosher options")
    
    if restriction_notes:
        recommendations += "DIETARY NOTES: We've focused on " + ", ".join(restriction_notes) + ".\n\n"
    
    # Add destination-specific recommendations
    if "paris" in destination:
        if preferences["vegetarian"] or preferences["vegan"]:
            recommendations += """
VEGETARIAN/VEGAN IN PARIS:
- Wild & The Moon - Trendy vegan cafe with multiple locations
- Le Potager du Marais - Traditional French cuisine veganized
- Hank Burger - Popular vegan burger spot
- Le Grenier de Notre-Dame - Oldest vegetarian restaurant in Paris

MUST-TRY DISHES:
- Ratatouille (vegetable stew)
- Socca (chickpea flatbread)
- Falafel from L'As du Fallafel in Le Marais
"""
        else:
            recommendations += """
CLASSIC PARISIAN FOOD:
- Croissants and pain au chocolat from local bakeries
- Steak frites at bistros like Le Relais de l'Entrecôte
- Duck confit at traditional brasseries
- French onion soup
- Escargot (snails) for the adventurous

TOP FOOD EXPERIENCES:
- Morning pastries at Du Pain et des Idées
- Picnic with cheese from Fromagerie Laurent Dubois
- Macarons from Pierre Hermé or Ladurée
- Wine and cheese tasting at La Vache dans les Vignes
"""
        
        if preferences["budget"]:
            recommendations += """
BUDGET-FRIENDLY OPTIONS:
- Crepe stands throughout the city
- Bakeries for affordable sandwiches (try jambon-beurre)
- Le Bouillon Chartier for classic French food at reasonable prices
- Rue Mouffetard market street for affordable eats
"""
        
        if preferences["fine_dining"]:
            recommendations += """
FINE DINING EXPERIENCES:
- Le Jules Verne - Eiffel Tower restaurant with spectacular views
- L'Ambroisie - Classic 3-Michelin-star French cuisine
- Septime - Modern French cuisine (reserve well in advance)
- Alain Ducasse au Plaza Athénée - Haute cuisine experience
"""
    
    elif "tokyo" in destination:
        if preferences["vegetarian"] or preferences["vegan"]:
            recommendations += """
VEGETARIAN/VEGAN IN TOKYO:
- Ain Soph Journey - Popular vegan restaurant chain
- T's TanTan - Vegan ramen in Tokyo Station
- 8ablish - Upscale vegan cuisine
- Saishoku Vegetarian - Traditional Buddhist vegetarian cuisine

MUST-TRY DISHES:
- Vegetable tempura
- Zaru soba (cold buckwheat noodles)
- Vegetarian sushi rolls
- Shojin ryori (Buddhist temple cuisine)
"""
        else:
            recommendations += """
CLASSIC TOKYO FOOD:
- Sushi at Tsukiji Outer Market
- Ramen at shops in Tokyo Station Ramen Street
- Tonkatsu (breaded pork cutlet)
- Monjayaki in Tsukishima
- Yakitori (grilled chicken skewers) in Omoide Yokocho

TOP FOOD EXPERIENCES:
- Early morning sushi breakfast at Tsukiji
- Izakaya hopping in Shinjuku
- Department store food halls (depachika)
- Themed cafes in Harajuku
"""
        
        if preferences["budget"]:
            recommendations += """
BUDGET-FRIENDLY OPTIONS:
- Conveyor belt sushi (kaitenzushi)
- Yoshinoya and other gyudon (beef bowl) chains
- Convenience store (konbini) meals - better than you'd expect!
- Standing soba shops
"""
        
        if preferences["street_food"]:
            recommendations += """
STREET FOOD & MARKETS:
- Takoyaki (octopus balls) in Asakusa
- Okonomiyaki in Harajuku
- Ameya-Yokocho Market in Ueno
- Nakamise Shopping Street in Asakusa
"""
    
    elif "bali" in destination:
        if preferences["vegetarian"] or preferences["vegan"]:
            recommendations += """
VEGETARIAN/VEGAN IN BALI:
- Zest in Ubud - Innovative vegan cuisine
- Peloton Supershop - Vegan cafe in Canggu
- Moksa in Ubud - Farm-to-table plant-based
- Clear Cafe - Vegetarian-friendly with many options

MUST-TRY DISHES:
- Gado-gado (vegetable salad with peanut sauce)
- Tempeh satay
- Sayur urap (vegetable salad with coconut)
- Jamu (traditional herbal drink)
"""
        else:
            recommendations += """
CLASSIC BALINESE FOOD:
- Babi guling (suckling pig) at Ibu Oka in Ubud
- Nasi campur (mixed rice plate)
- Betutu (slow-cooked spiced chicken or duck)
- Sate lilit (minced seafood satay)
- Lawar (mixed vegetables with meat)

TOP FOOD EXPERIENCES:
- Seafood dinner on Jimbaran Beach
- Traditional Balinese cooking class
- Sunday brunch at Ku De Ta in Seminyak
- Sunset drinks at Single Fin in Uluwatu
"""
        
        if preferences["budget"]:
            recommendations += """
BUDGET-FRIENDLY OPTIONS:
- Local warungs (small family-owned restaurants)
- Nasi campur stands (look for busy ones with locals)
- Pasar malam (night markets)
- Nasi jinggo (small rice packets with sides)
"""
        
        if preferences["fine_dining"]:
            recommendations += """
FINE DINING EXPERIENCES:
- Locavore in Ubud - Inventive cuisine using local ingredients
- Mejekawi by Ku De Ta - Tasting kitchen concept
- Apéritif - Colonial-inspired fine dining in Ubud
- Room4Dessert - Unique dessert-focused tasting menu
"""
    
    else:
        # Generic recommendations for other destinations
        recommendations += """
GENERAL FOOD RECOMMENDATIONS:

- Seek out local specialties unique to the region
- Visit local markets for fresh produce and authentic street food
- Ask hotel staff or locals for their favorite restaurants
- Try a mix of street food and sit-down restaurants for varied experiences
- Consider a food tour early in your trip to discover good spots

LOCAL FOOD APPS:
- TripAdvisor or Yelp for tourist-friendly options
- Google Maps for nearby suggestions with reviews
- Consider local food apps if available for your destination
"""
    
    if preferences["allergies"]:
        recommendations += """

ALLERGY INFORMATION:
- Carry an allergy translation card in the local language
- Research common allergens in local cuisine before your trip
- Learn how to ask about allergens in the local language
- Consider dining at more tourist-friendly restaurants where staff may speak English
"""
    
    return recommendations

if __name__ == "__main__":
    dietary_agent.run() 