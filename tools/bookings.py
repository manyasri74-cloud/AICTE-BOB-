"""
Booking Management Tool
Handles trip bookings, manages alerts, and stores travel plans.
"""

import json
import uuid
import datetime
from typing import Optional


# In-memory store (in production, this would be a database)
_bookings_store: dict = {}


class BookingTool:
    """Tool for managing travel bookings and alerts."""

    def create_booking(
        self,
        destination: str,
        start_date: str,
        end_date: str,
        travellers: int = 1,
        budget_usd: Optional[float] = None,
        notes: Optional[str] = None,
    ) -> dict:
        """
        Create a new travel booking record.

        Args:
            destination: Travel destination
            start_date: Trip start date (YYYY-MM-DD)
            end_date: Trip end date (YYYY-MM-DD)
            travellers: Number of travellers
            budget_usd: Total budget in USD
            notes: Additional notes
        """
        booking_id = str(uuid.uuid4())[:8].upper()
        booking = {
            "booking_id": booking_id,
            "destination": destination,
            "start_date": start_date,
            "end_date": end_date,
            "travellers": travellers,
            "budget_usd": budget_usd,
            "notes": notes,
            "status": "CONFIRMED",
            "created_at": datetime.datetime.now().isoformat(),
            "alerts": [],
        }
        _bookings_store[booking_id] = booking
        return booking

    def get_booking(self, booking_id: str) -> Optional[dict]:
        """Retrieve a booking by ID."""
        return _bookings_store.get(booking_id.upper())

    def list_bookings(self) -> list:
        """List all active bookings."""
        return list(_bookings_store.values())

    def add_alert(self, booking_id: str, alert_message: str) -> bool:
        """Add an alert/notification to a booking."""
        booking = _bookings_store.get(booking_id.upper())
        if booking:
            booking["alerts"].append({
                "message": alert_message,
                "timestamp": datetime.datetime.now().isoformat(),
            })
            return True
        return False

    def cancel_booking(self, booking_id: str) -> bool:
        """Cancel a booking."""
        booking = _bookings_store.get(booking_id.upper())
        if booking:
            booking["status"] = "CANCELLED"
            return True
        return False

    def get_trip_summary(self, booking_id: str) -> Optional[dict]:
        """Get a full trip summary for a booking."""
        booking = self.get_booking(booking_id)
        if not booking:
            return None

        try:
            start = datetime.date.fromisoformat(booking["start_date"])
            end = datetime.date.fromisoformat(booking["end_date"])
            duration = (end - start).days + 1
        except Exception:
            duration = 0

        return {
            **booking,
            "duration_days": duration,
            "days_until_trip": self._days_until(booking["start_date"]),
        }

    def _days_until(self, start_date: str) -> int:
        """Calculate days until trip starts."""
        try:
            start = datetime.date.fromisoformat(start_date)
            delta = (start - datetime.date.today()).days
            return max(delta, 0)
        except Exception:
            return 0

    def format_booking_for_display(self, booking: dict) -> str:
        """Format booking details as readable text."""
        lines = [
            f"✅ **Booking Confirmed!**",
            f"",
            f"📋 **Booking ID:** `{booking['booking_id']}`",
            f"📍 **Destination:** {booking['destination']}",
            f"📅 **Dates:** {booking['start_date']} → {booking['end_date']}",
            f"👥 **Travellers:** {booking['travellers']}",
            f"💰 **Budget:** ${booking.get('budget_usd', 'N/A')}",
            f"📊 **Status:** {booking['status']}",
        ]
        if booking.get("days_until_trip") is not None:
            days = booking.get("days_until_trip", 0)
            lines.append(f"⏳ **Days Until Trip:** {days} days")
        if booking.get("notes"):
            lines.append(f"📝 **Notes:** {booking['notes']}")
        if booking.get("alerts"):
            lines.append("\n🔔 **Alerts:**")
            for alert in booking["alerts"]:
                lines.append(f"  • {alert['message']}")
        return "\n".join(lines)
