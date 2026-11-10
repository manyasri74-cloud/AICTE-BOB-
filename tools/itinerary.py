"""
Itinerary Builder Tool
Creates day-by-day travel plans based on destination, duration, and interests.
"""

from typing import Optional
import datetime


# Activity templates per destination type
ACTIVITY_TEMPLATES = {
    "beach": {
        "morning": ["Sunrise walk on the beach", "Snorkeling / Scuba diving", "Kayaking tour", "Dolphin watching boat trip"],
        "afternoon": ["Visit local market", "Beach volleyball", "Jet skiing / Parasailing", "Island hopping tour"],
        "evening": ["Sunset cruise", "Beachside dinner", "Beach bonfire", "Local seafood at shack"],
    },
    "cultural": {
        "morning": ["Visit main historical site", "Guided heritage walk", "Temple / Church tour", "Museum visit"],
        "afternoon": ["Local food tasting tour", "Traditional craft workshop", "Art gallery visit", "Palace or fort tour"],
        "evening": ["Cultural performance / Folk dance", "Night bazaar shopping", "Fine dining with local cuisine", "Light & sound show"],
    },
    "adventure": {
        "morning": ["Sunrise trek", "River rafting", "Mountain biking", "Rock climbing session"],
        "afternoon": ["Paragliding / Zip-lining", "Jungle safari", "Waterfall hike", "Camping setup"],
        "evening": ["Campfire dinner", "Stargazing", "Local village interaction", "Birdwatching at dusk"],
    },
    "city": {
        "morning": ["City skyline viewpoint visit", "Iconic landmark tour", "Breakfast at famous café", "Museum or gallery visit"],
        "afternoon": ["Shopping district exploration", "Local food hall tour", "Street art walk", "Neighbourhood exploration"],
        "evening": ["Rooftop bar / dinner", "Night markets", "Live music venue", "Cruise along city waterway"],
    },
    "nature": {
        "morning": ["Wildlife safari / birdwatching", "Waterfall hike", "Plantation tour", "Sunrise nature walk"],
        "afternoon": ["Picnic in national park", "Boat ride on lake / river", "Botanical garden visit", "Cycling through countryside"],
        "evening": ["Bonfire with local dinner", "Stargazing in open field", "Resort spa & relaxation", "Sunset viewpoint"],
    },
}

DAY_LABELS = ["Arrival & Orientation", "Exploration", "Deep Dive", "Hidden Gems", "Local Experiences", "Leisure", "Departure"]


class ItineraryTool:
    """Tool for building day-by-day travel itineraries."""

    def build_itinerary(
        self,
        destination: str,
        duration_days: int = 5,
        destination_type: str = "cultural",
        start_date: Optional[str] = None,
        interests: Optional[list] = None,
    ) -> dict:
        """
        Build a detailed day-by-day itinerary.

        Args:
            destination: Name of the destination
            duration_days: Number of days for the trip
            destination_type: Type of destination (beach/cultural/adventure/city/nature)
            start_date: Trip start date (YYYY-MM-DD)
            interests: Specific interests of the traveller
        """
        template = ACTIVITY_TEMPLATES.get(destination_type, ACTIVITY_TEMPLATES["cultural"])
        mornings = template["morning"]
        afternoons = template["afternoon"]
        evenings = template["evening"]

        if start_date:
            try:
                trip_start = datetime.date.fromisoformat(start_date)
            except ValueError:
                trip_start = datetime.date.today() + datetime.timedelta(days=7)
        else:
            trip_start = datetime.date.today() + datetime.timedelta(days=7)

        days = []
        for day_num in range(1, duration_days + 1):
            current_date = trip_start + datetime.timedelta(days=day_num - 1)
            label_index = min(day_num - 1, len(DAY_LABELS) - 1)
            label = DAY_LABELS[label_index]

            if day_num == 1:
                activities = {
                    "morning": f"Arrive at {destination} — check in to accommodation",
                    "afternoon": f"Orientation walk around {destination} city centre / neighbourhood",
                    "evening": f"Welcome dinner at a popular local restaurant in {destination}",
                }
            elif day_num == duration_days:
                activities = {
                    "morning": "Pack up & have breakfast at the hotel",
                    "afternoon": f"Last-minute souvenir shopping in {destination}",
                    "evening": f"Transfer to airport / station — depart from {destination}",
                }
            else:
                idx = (day_num - 2) % len(mornings)
                activities = {
                    "morning": mornings[idx],
                    "afternoon": afternoons[idx % len(afternoons)],
                    "evening": evenings[idx % len(evenings)],
                }

            days.append({
                "day": day_num,
                "date": current_date.strftime("%A, %d %B %Y"),
                "label": label,
                "activities": activities,
            })

        return {
            "destination": destination,
            "duration_days": duration_days,
            "start_date": trip_start.isoformat(),
            "end_date": (trip_start + datetime.timedelta(days=duration_days - 1)).isoformat(),
            "type": destination_type,
            "days": days,
        }

    def format_for_display(self, itinerary: dict) -> str:
        """Format itinerary as readable text."""
        lines = [
            f"🗺️ **{itinerary['duration_days']}-Day Itinerary for {itinerary['destination']}**",
            f"📅 {itinerary['start_date']} → {itinerary['end_date']}",
            "",
        ]
        for day in itinerary["days"]:
            lines.append(f"---\n**Day {day['day']} – {day['label']}** | {day['date']}")
            acts = day["activities"]
            lines.append(f"  🌅 Morning: {acts['morning']}")
            lines.append(f"  ☀️ Afternoon: {acts['afternoon']}")
            lines.append(f"  🌙 Evening: {acts['evening']}")
            lines.append("")
        return "\n".join(lines)
