"""
Transport Recommendation Tool
Recommends transport options (flights, trains, buses, local travel)
based on origin, destination, and budget.
"""

from typing import Optional


TRANSPORT_OPTIONS = {
    "flight": {
        "icon": "✈️",
        "pros": ["Fastest", "Long distances", "Comfortable"],
        "cons": ["Expensive", "Airport time overhead", "Carbon footprint"],
        "book_via": ["Google Flights", "MakeMyTrip", "Skyscanner", "IRCTC Air"],
    },
    "train": {
        "icon": "🚆",
        "pros": ["Scenic views", "City-centre to city-centre", "Eco-friendly", "Affordable"],
        "cons": ["Slower than flights", "Limited routes", "Advance booking needed"],
        "book_via": ["IRCTC (India)", "Eurail (Europe)", "JR Pass (Japan)", "RailEurope"],
    },
    "bus": {
        "icon": "🚌",
        "pros": ["Budget-friendly", "Flexible routes", "Point-to-point service"],
        "cons": ["Slowest", "Less comfortable on long trips", "Traffic dependent"],
        "book_via": ["RedBus (India)", "FlixBus (Europe)", "Greyhound (USA)", "Local operators"],
    },
    "car_rental": {
        "icon": "🚗",
        "pros": ["Maximum flexibility", "Door-to-door", "Great for road trips"],
        "cons": ["Parking challenges in cities", "Driving license required", "Fuel cost"],
        "book_via": ["Zoomcar (India)", "Hertz", "Avis", "Enterprise"],
    },
    "ferry": {
        "icon": "⛴️",
        "pros": ["Scenic water routes", "Often carries vehicles", "Unique experience"],
        "cons": ["Weather dependent", "Limited routes", "Slower than air"],
        "book_via": ["Local port operators", "Direct Line Cruises", "Brittany Ferries"],
    },
}

LOCAL_TRANSPORT = {
    "metro": {"icon": "🚇", "description": "Best for city centre navigation. Cheap and fast."},
    "auto_rickshaw": {"icon": "🛺", "description": "Iconic in Indian cities. Affordable for short trips."},
    "taxi": {"icon": "🚕", "description": "Door-to-door convenience. Book via Ola, Uber, or local taxis."},
    "cycle_rental": {"icon": "🚲", "description": "Eco-friendly and great for exploring at a relaxed pace."},
    "tuk_tuk": {"icon": "🛵", "description": "Popular in Southeast Asia. Fun and budget-friendly."},
    "cable_car": {"icon": "🚡", "description": "For hilly regions and scenic mountain routes."},
}


class TransportTool:
    """Tool for recommending transport options."""

    def recommend_transport(
        self,
        origin: str,
        destination: str,
        budget: Optional[str] = "medium",
        duration_hours: Optional[float] = None,
    ) -> dict:
        """
        Recommend transport modes based on route and preferences.

        Args:
            origin: Departure city/location
            destination: Arrival city/location
            budget: Budget level (low/medium/high)
            duration_hours: Available travel time in hours
        """
        recommendations = []

        # Budget-based filtering
        if budget == "low":
            priorities = ["bus", "train", "ferry", "flight"]
        elif budget == "high":
            priorities = ["flight", "car_rental", "train", "ferry", "bus"]
        else:
            priorities = ["train", "flight", "bus", "car_rental", "ferry"]

        for mode in priorities:
            options = TRANSPORT_OPTIONS[mode]
            recommendations.append({
                "mode": mode.replace("_", " ").title(),
                "icon": options["icon"],
                "pros": options["pros"],
                "cons": options["cons"],
                "book_via": options["book_via"],
            })

        return {
            "origin": origin,
            "destination": destination,
            "recommendations": recommendations[:3],  # Top 3 options
            "local_transport": self._get_local_options(destination),
        }

    def _get_local_options(self, destination: str) -> list:
        """Get relevant local transport options for a destination."""
        dest_lower = destination.lower()

        if any(city in dest_lower for city in ["goa", "mumbai", "delhi", "bangalore", "hyderabad", "kolkata"]):
            return [LOCAL_TRANSPORT["metro"], LOCAL_TRANSPORT["auto_rickshaw"], LOCAL_TRANSPORT["taxi"]]
        elif any(city in dest_lower for city in ["bali", "bangkok", "phuket", "kathmandu"]):
            return [LOCAL_TRANSPORT["tuk_tuk"], LOCAL_TRANSPORT["taxi"], LOCAL_TRANSPORT["cycle_rental"]]
        elif any(city in dest_lower for city in ["manali", "darjeeling", "shimla", "queenstown"]):
            return [LOCAL_TRANSPORT["taxi"], LOCAL_TRANSPORT["cable_car"], LOCAL_TRANSPORT["cycle_rental"]]
        else:
            return [LOCAL_TRANSPORT["taxi"], LOCAL_TRANSPORT["metro"], LOCAL_TRANSPORT["cycle_rental"]]

    def format_for_display(self, transport_info: dict) -> str:
        """Format transport options as readable text."""
        lines = [
            f"🗺️ **Transport Options: {transport_info['origin']} → {transport_info['destination']}**",
            "",
            "**Recommended Modes:**",
        ]
        for i, rec in enumerate(transport_info["recommendations"], 1):
            lines.append(f"\n{rec['icon']} **{i}. {rec['mode']}**")
            lines.append(f"  ✅ Pros: {', '.join(rec['pros'][:2])}")
            lines.append(f"  ❌ Cons: {', '.join(rec['cons'][:2])}")
            lines.append(f"  📱 Book via: {', '.join(rec['book_via'][:2])}")

        lines.append("\n**Local Getting Around:**")
        for local in transport_info.get("local_transport", []):
            lines.append(f"  {local['icon']} {local['description']}")

        return "\n".join(lines)
