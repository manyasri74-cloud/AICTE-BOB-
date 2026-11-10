"""
Accommodation Recommendation Tool
Suggests hotels, hostels, homestays, and resorts based on
destination, budget, and traveller type.
"""

from typing import Optional


ACCOMMODATION_TYPES = {
    "budget_hostel": {
        "type": "Budget Hostel / Dormitory",
        "icon": "🏨",
        "price_range_usd": "$5–$20/night",
        "ideal_for": ["Solo backpackers", "Young travellers", "Social experiences"],
        "amenities": ["Shared bathrooms", "Common kitchen", "Lockers", "Free Wi-Fi"],
        "book_via": ["Hostelworld", "Booking.com", "HostelBookers"],
    },
    "budget_hotel": {
        "type": "Budget Hotel / Guesthouse",
        "icon": "🏩",
        "price_range_usd": "$20–$60/night",
        "ideal_for": ["Couples", "Budget travellers", "Short stays"],
        "amenities": ["Private room", "Attached bathroom", "Wi-Fi", "AC/Fan"],
        "book_via": ["MakeMyTrip", "OYO", "Booking.com", "Goibibo"],
    },
    "mid_range_hotel": {
        "type": "Mid-Range Hotel (3–4 Star)",
        "icon": "🏪",
        "price_range_usd": "$60–$150/night",
        "ideal_for": ["Families", "Business travellers", "Comfort seekers"],
        "amenities": ["Room service", "Swimming pool", "Restaurant", "Gym", "Concierge"],
        "book_via": ["Hotels.com", "Booking.com", "Expedia", "Agoda"],
    },
    "luxury_hotel": {
        "type": "Luxury Hotel (5 Star / Resort)",
        "icon": "🏰",
        "price_range_usd": "$150–$500+/night",
        "ideal_for": ["Honeymoon couples", "Luxury travellers", "Special occasions"],
        "amenities": ["Spa & Wellness", "Butler service", "Fine dining", "Private pool", "Airport pickup"],
        "book_via": ["Taj Hotels", "Marriott", "IHG", "Hilton", "Expedia"],
    },
    "homestay": {
        "type": "Homestay / Airbnb",
        "icon": "🏠",
        "price_range_usd": "$25–$100/night",
        "ideal_for": ["Families", "Long stays", "Cultural immersion"],
        "amenities": ["Full kitchen", "Local host guidance", "Home-cooked meals (optional)", "Wi-Fi"],
        "book_via": ["Airbnb", "Vrbo", "Homestay.com"],
    },
    "eco_resort": {
        "type": "Eco-Resort / Nature Camp",
        "icon": "🌿",
        "price_range_usd": "$40–$200/night",
        "ideal_for": ["Nature lovers", "Adventure travellers", "Sustainability-conscious"],
        "amenities": ["Jungle views", "Organic meals", "Nature walks", "Campfire"],
        "book_via": ["Booking.com", "Direct resort websites", "EcoHotels.com"],
    },
}

BUDGET_TO_TYPE = {
    "low": ["budget_hostel", "budget_hotel"],
    "medium": ["budget_hotel", "mid_range_hotel", "homestay"],
    "high": ["mid_range_hotel", "luxury_hotel", "eco_resort"],
    "any": list(ACCOMMODATION_TYPES.keys()),
}


class AccommodationTool:
    """Tool for recommending accommodation options."""

    def recommend_accommodation(
        self,
        destination: str,
        budget: Optional[str] = "medium",
        traveller_type: Optional[str] = None,
        duration_nights: Optional[int] = 5,
    ) -> dict:
        """
        Recommend accommodation based on destination and preferences.

        Args:
            destination: Travel destination
            budget: Budget level (low/medium/high/any)
            traveller_type: Solo, couple, family, group, business
            duration_nights: Number of nights
        """
        budget_key = (budget or "medium").lower()
        type_keys = BUDGET_TO_TYPE.get(budget_key, BUDGET_TO_TYPE["any"])

        recommendations = []
        for key in type_keys:
            acc = ACCOMMODATION_TYPES[key].copy()
            acc["key"] = key

            # Calculate estimated total
            price_str = acc["price_range_usd"].replace("$", "").replace("/night", "").replace("+", "")
            try:
                if "–" in price_str:
                    low, high = price_str.split("–")
                    avg_per_night = (int(low) + int(high)) / 2
                else:
                    avg_per_night = int(price_str)
            except ValueError:
                avg_per_night = 75

            acc["estimated_total_usd"] = round(avg_per_night * (duration_nights or 5), 2)
            recommendations.append(acc)

        return {
            "destination": destination,
            "duration_nights": duration_nights,
            "budget": budget,
            "traveller_type": traveller_type or "general",
            "options": recommendations,
            "pro_tips": self._get_pro_tips(destination, budget),
        }

    def _get_pro_tips(self, destination: str, budget: Optional[str]) -> list:
        """Return booking tips for the destination."""
        tips = [
            "📅 Book at least 2–4 weeks in advance for better rates.",
            "💳 Check for free cancellation policies before confirming.",
            "⭐ Read recent guest reviews for up-to-date info.",
            "📍 Choose accommodation close to main attractions to save on transport.",
        ]
        if budget == "low":
            tips.append("🎒 Hostels often have private rooms too — ask the front desk!")
        if budget == "high":
            tips.append("✈️ Ask about complimentary airport transfers when booking luxury hotels.")
        return tips

    def format_for_display(self, acc_info: dict) -> str:
        """Format accommodation options as readable text."""
        lines = [
            f"🏨 **Accommodation in {acc_info['destination']}** ({acc_info['duration_nights']} nights)",
            f"👤 Traveller type: {acc_info['traveller_type'].title()}  |  💰 Budget: {acc_info['budget'].title()}",
            "",
        ]
        for opt in acc_info["options"]:
            lines.append(f"{opt['icon']} **{opt['type']}**")
            lines.append(f"  💵 {opt['price_range_usd']}  |  Trip estimate: ~${opt['estimated_total_usd']}")
            lines.append(f"  👥 Ideal for: {', '.join(opt['ideal_for'][:2])}")
            lines.append(f"  🛎️ Amenities: {', '.join(opt['amenities'][:3])}")
            lines.append(f"  📱 Book via: {', '.join(opt['book_via'][:2])}")
            lines.append("")

        lines.append("💡 **Pro Tips:**")
        for tip in acc_info["pro_tips"]:
            lines.append(f"  {tip}")

        return "\n".join(lines)
