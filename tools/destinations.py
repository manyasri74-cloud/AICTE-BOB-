"""
Destination Discovery Tool
Suggests travel destinations based on user preferences, budget, and interests.
"""

from typing import Optional


# Curated destination knowledge base
DESTINATIONS = {
    "beach": [
        {
            "name": "Goa, India",
            "country": "India",
            "type": "beach",
            "budget": "low",
            "best_season": "November–February",
            "highlights": ["Beaches", "Nightlife", "Portuguese heritage", "Water sports"],
            "avg_daily_cost_usd": 40,
            "currency": "INR",
            "language": "Konkani, English",
            "visa_required": False,
        },
        {
            "name": "Bali, Indonesia",
            "country": "Indonesia",
            "type": "beach",
            "budget": "low-medium",
            "best_season": "April–October",
            "highlights": ["Temples", "Rice terraces", "Surfing", "Nightlife"],
            "avg_daily_cost_usd": 55,
            "currency": "IDR",
            "language": "Balinese, Indonesian",
            "visa_required": False,
        },
        {
            "name": "Maldives",
            "country": "Maldives",
            "type": "beach",
            "budget": "high",
            "best_season": "November–April",
            "highlights": ["Overwater bungalows", "Snorkelling", "Coral reefs", "Luxury resorts"],
            "avg_daily_cost_usd": 300,
            "currency": "MVR",
            "language": "Dhivehi, English",
            "visa_required": False,
        },
        {
            "name": "Phuket, Thailand",
            "country": "Thailand",
            "type": "beach",
            "budget": "low-medium",
            "best_season": "November–April",
            "highlights": ["White sand beaches", "Thai cuisine", "Islands", "Diving"],
            "avg_daily_cost_usd": 60,
            "currency": "THB",
            "language": "Thai",
            "visa_required": False,
        },
    ],
    "cultural": [
        {
            "name": "Kyoto, Japan",
            "country": "Japan",
            "type": "cultural",
            "budget": "medium-high",
            "best_season": "March–May, October–November",
            "highlights": ["Temples", "Geisha culture", "Cherry blossoms", "Traditional food"],
            "avg_daily_cost_usd": 120,
            "currency": "JPY",
            "language": "Japanese",
            "visa_required": True,
        },
        {
            "name": "Rome, Italy",
            "country": "Italy",
            "type": "cultural",
            "budget": "medium-high",
            "best_season": "April–June, September–October",
            "highlights": ["Colosseum", "Vatican", "Renaissance art", "Italian cuisine"],
            "avg_daily_cost_usd": 130,
            "currency": "EUR",
            "language": "Italian",
            "visa_required": True,
        },
        {
            "name": "Rajasthan, India",
            "country": "India",
            "type": "cultural",
            "budget": "low",
            "best_season": "October–March",
            "highlights": ["Forts", "Palaces", "Desert safari", "Traditional crafts"],
            "avg_daily_cost_usd": 35,
            "currency": "INR",
            "language": "Hindi, Rajasthani",
            "visa_required": False,
        },
        {
            "name": "Istanbul, Turkey",
            "country": "Turkey",
            "type": "cultural",
            "budget": "medium",
            "best_season": "April–May, September–October",
            "highlights": ["Hagia Sophia", "Grand Bazaar", "Bosphorus", "Ottoman history"],
            "avg_daily_cost_usd": 70,
            "currency": "TRY",
            "language": "Turkish",
            "visa_required": True,
        },
    ],
    "adventure": [
        {
            "name": "Manali, India",
            "country": "India",
            "type": "adventure",
            "budget": "low",
            "best_season": "October–June",
            "highlights": ["Trekking", "River rafting", "Snow sports", "Himalayan views"],
            "avg_daily_cost_usd": 30,
            "currency": "INR",
            "language": "Hindi",
            "visa_required": False,
        },
        {
            "name": "Queenstown, New Zealand",
            "country": "New Zealand",
            "type": "adventure",
            "budget": "high",
            "best_season": "December–February",
            "highlights": ["Bungee jumping", "Skydiving", "Skiing", "Fjords"],
            "avg_daily_cost_usd": 200,
            "currency": "NZD",
            "language": "English",
            "visa_required": True,
        },
        {
            "name": "Nepal (Kathmandu & Everest Region)",
            "country": "Nepal",
            "type": "adventure",
            "budget": "low-medium",
            "best_season": "October–November, March–May",
            "highlights": ["Everest Base Camp trek", "Annapurna Circuit", "Temples", "Monasteries"],
            "avg_daily_cost_usd": 45,
            "currency": "NPR",
            "language": "Nepali",
            "visa_required": True,
        },
    ],
    "city": [
        {
            "name": "Singapore",
            "country": "Singapore",
            "type": "city",
            "budget": "high",
            "best_season": "February–April",
            "highlights": ["Marina Bay Sands", "Gardens by the Bay", "Food culture", "Shopping"],
            "avg_daily_cost_usd": 180,
            "currency": "SGD",
            "language": "English, Mandarin",
            "visa_required": False,
        },
        {
            "name": "Dubai, UAE",
            "country": "UAE",
            "type": "city",
            "budget": "high",
            "best_season": "November–March",
            "highlights": ["Burj Khalifa", "Desert safari", "Shopping malls", "Architecture"],
            "avg_daily_cost_usd": 200,
            "currency": "AED",
            "language": "Arabic, English",
            "visa_required": True,
        },
        {
            "name": "Bangkok, Thailand",
            "country": "Thailand",
            "type": "city",
            "budget": "low",
            "best_season": "November–February",
            "highlights": ["Temples", "Street food", "Nightlife", "Floating markets"],
            "avg_daily_cost_usd": 45,
            "currency": "THB",
            "language": "Thai",
            "visa_required": False,
        },
    ],
    "nature": [
        {
            "name": "Coorg, India",
            "country": "India",
            "type": "nature",
            "budget": "low",
            "best_season": "October–May",
            "highlights": ["Coffee plantations", "Waterfalls", "Wildlife", "Trekking"],
            "avg_daily_cost_usd": 30,
            "currency": "INR",
            "language": "Kodava, Kannada",
            "visa_required": False,
        },
        {
            "name": "Patagonia, Argentina/Chile",
            "country": "Argentina/Chile",
            "type": "nature",
            "budget": "high",
            "best_season": "November–March",
            "highlights": ["Torres del Paine", "Glaciers", "Hiking", "Wildlife"],
            "avg_daily_cost_usd": 150,
            "currency": "ARS/CLP",
            "language": "Spanish",
            "visa_required": False,
        },
    ],
}

BUDGET_MAP = {
    "low": lambda cost: cost <= 50,
    "medium": lambda cost: 50 < cost <= 120,
    "high": lambda cost: cost > 120,
    "any": lambda cost: True,
}


class DestinationTool:
    """Tool for suggesting and filtering travel destinations."""

    def suggest_destinations(
        self,
        interest: Optional[str] = None,
        budget: Optional[str] = "any",
        duration_days: Optional[int] = 7,
    ) -> list:
        """
        Suggest destinations based on interest and budget.

        Args:
            interest: Type of travel (beach, cultural, adventure, city, nature)
            budget: Budget level (low, medium, high, any)
            duration_days: Trip duration in days
        """
        results = []
        budget_key = (budget or "any").lower()
        budget_filter = BUDGET_MAP.get(budget_key, BUDGET_MAP["any"])

        if interest:
            interest_lower = interest.lower()
            # Check if the interest matches a category
            for category, destinations in DESTINATIONS.items():
                if interest_lower in category or category in interest_lower:
                    for dest in destinations:
                        if budget_filter(dest["avg_daily_cost_usd"]):
                            dest_copy = dest.copy()
                            dest_copy["estimated_total_usd"] = dest["avg_daily_cost_usd"] * (duration_days or 7)
                            results.append(dest_copy)
        else:
            # Return all destinations filtered by budget
            for destinations in DESTINATIONS.values():
                for dest in destinations:
                    if budget_filter(dest["avg_daily_cost_usd"]):
                        dest_copy = dest.copy()
                        dest_copy["estimated_total_usd"] = dest["avg_daily_cost_usd"] * (duration_days or 7)
                        results.append(dest_copy)

        # Sort by daily cost ascending
        results.sort(key=lambda x: x["avg_daily_cost_usd"])
        return results[:6]  # Return top 6 results

    def get_destination_info(self, destination_name: str) -> Optional[dict]:
        """Get detailed information about a specific destination."""
        name_lower = destination_name.lower()
        for destinations in DESTINATIONS.values():
            for dest in destinations:
                if name_lower in dest["name"].lower() or dest["name"].lower() in name_lower:
                    return dest
        return None

    def format_for_display(self, destinations: list) -> str:
        """Format destination list as readable text."""
        if not destinations:
            return "No destinations found matching your criteria."

        lines = ["🌍 **Recommended Destinations:**\n"]
        for i, dest in enumerate(destinations, 1):
            lines.append(f"**{i}. {dest['name']}** ({dest['country']})")
            lines.append(f"   📅 Best Season: {dest['best_season']}")
            lines.append(f"   💰 ~${dest['avg_daily_cost_usd']}/day | Trip estimate: ~${dest.get('estimated_total_usd', 'N/A')}")
            lines.append(f"   ✨ Highlights: {', '.join(dest['highlights'][:3])}")
            lines.append(f"   🌐 Language: {dest['language']}")
            lines.append("")
        return "\n".join(lines)
