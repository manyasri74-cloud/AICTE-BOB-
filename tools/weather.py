"""
Weather Tool
Provides real-time weather info and forecasts for travel planning.
Wraps IBM Cloud + OpenWeatherMap integration.
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from ibm_client import WeatherClient


PACKING_SUGGESTIONS = {
    "sunny": ["Sunscreen (SPF 50+)", "Sunglasses", "Light cotton clothes", "Hat/Cap", "Water bottle"],
    "cloudy": ["Light jacket", "Comfortable walking shoes", "Umbrella (just in case)"],
    "rain": ["Waterproof jacket / Raincoat", "Umbrella", "Waterproof shoes", "Extra dry bags for electronics"],
    "snow": ["Heavy winter coat", "Thermal innerwear", "Snow boots", "Gloves & Scarf", "Beanie/Woollen hat"],
    "hot": ["Light breathable clothing", "Electrolyte drinks", "Cooling towel", "Sunscreen", "Sunglasses"],
    "cold": ["Layered clothing", "Warm jacket", "Scarf & gloves", "Thermos for hot drinks"],
}


class WeatherTool:
    """Tool for getting weather data and providing travel advice."""

    def __init__(self):
        self._client = WeatherClient()

    def get_weather_info(self, city: str) -> dict:
        """Get current weather and packing suggestions for a city."""
        weather = self._client.get_weather(city)
        forecast = self._client.get_forecast(city)
        packing = self._get_packing_tips(weather)
        travel_advice = self._get_travel_advice(weather)

        return {
            "current": weather,
            "forecast": forecast,
            "packing_tips": packing,
            "travel_advice": travel_advice,
        }

    def _get_packing_tips(self, weather: dict) -> list:
        """Generate packing tips based on weather conditions."""
        description = weather.get("description", "").lower()
        temp = weather.get("temperature", 20)

        tips = []
        if "rain" in description or "drizzle" in description:
            tips.extend(PACKING_SUGGESTIONS["rain"])
        elif "snow" in description:
            tips.extend(PACKING_SUGGESTIONS["snow"])
        elif "sunny" in description or "clear" in description:
            tips.extend(PACKING_SUGGESTIONS["sunny"])
        else:
            tips.extend(PACKING_SUGGESTIONS["cloudy"])

        if temp > 30:
            tips.extend(PACKING_SUGGESTIONS["hot"])
        elif temp < 10:
            tips.extend(PACKING_SUGGESTIONS["cold"])

        # Deduplicate while preserving order
        seen = set()
        unique_tips = []
        for tip in tips:
            if tip not in seen:
                seen.add(tip)
                unique_tips.append(tip)
        return unique_tips[:8]

    def _get_travel_advice(self, weather: dict) -> str:
        """Generate contextual travel advice based on weather."""
        temp = weather.get("temperature", 20)
        description = weather.get("description", "").lower()

        if temp > 35:
            return "Very hot weather expected. Plan outdoor activities in early morning or evening. Stay hydrated!"
        elif temp > 25:
            return "Warm and pleasant weather. Great for outdoor sightseeing. Carry water and sunscreen."
        elif temp > 15:
            return "Comfortable weather. Light layers recommended. Perfect for walking tours."
        elif temp > 5:
            return "Cool weather. Pack warm clothes and a jacket. Hot beverages will be your best friend."
        else:
            return "Cold weather expected. Bundle up with heavy winter clothing. Check for snow advisories."

    def format_for_display(self, weather_info: dict) -> str:
        """Format weather info as readable text."""
        current = weather_info["current"]
        forecast = weather_info["forecast"]
        tips = weather_info["packing_tips"]
        advice = weather_info["travel_advice"]

        lines = [
            f"🌤️ **Weather in {current['city']}** ({current.get('country', '')})",
            f"🌡️ Temperature: **{current['temperature']}°C** (Feels like {current['feels_like']}°C)",
            f"🌥️ Conditions: {current['description']}",
            f"💧 Humidity: {current['humidity']}%  |  💨 Wind: {current['wind_speed']} m/s",
            f"👁️ Visibility: {current['visibility']} km",
            "",
            f"💡 **Travel Tip:** {advice}",
            "",
            "📦 **Packing Suggestions:**",
        ]
        for tip in tips:
            lines.append(f"  • {tip}")

        if forecast:
            lines.append("\n📅 **5-Day Forecast:**")
            for day in forecast:
                lines.append(f"  {day['date']}: {day['temp']}°C — {day['description']}")

        return "\n".join(lines)
