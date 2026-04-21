from backend.models.hotel import Hotel
from backend.models.booking import Booking
from backend.utils.formatters import format_amenities, format_currency

class MessageTemplates:
    @staticmethod
    def welcome_message() -> str:
        return (
            "🏨 *Welcome to the Global Hotel Search Bot!* 🏨\n\n"
            "I'm your personal travel assistant. Find the best hotels across the world and book your stay in seconds!\n\n"
            "*Key Features:*\n"
            "🔍 Search by city\n"
            "⭐ Filter by rating & price\n"
            "📅 Easy mock booking flow\n"
            "🏛️ Detailed hotel views\n\n"
            "Use /search to start, or /cities to see where we operate!"
        )

    @staticmethod
    def help_message() -> str:
        return (
            "🛠️ *Available Commands:*\n\n"
            "🚀 /start - Welcome message\n"
            "🔍 /search - Start searching for hotels\n"
            "📍 /cities - List all supported cities\n"
            "📖 /help - Show this guide\n"
            "❌ /cancel - Stop current operation"
        )

    @staticmethod
    def city_list_message(cities: list) -> str:
        city_text = "\n".join([f"📍 {city}" for city in cities])
        return (
            "🌍 *Our Supported Cities:*\n\n"
            f"{city_text}\n\n"
            "Type /search to find a hotel in one of these cities!"
        )

    @staticmethod
    def hotel_card(hotel: Hotel) -> str:
        return (
            f"{hotel.image_emoji} *{hotel.name}*\n"
            f"📍 {hotel.city}, {hotel.country}\n"
            f"💰 {format_currency(hotel.price_per_night)} / night {hotel.price_indicator}\n"
            f"⭐ {hotel.rating} {hotel.star_display}"
        )

    @staticmethod
    def hotel_detail(hotel: Hotel) -> str:
        amenities = format_amenities(hotel.amenities)
        return (
            f"{hotel.image_emoji} *{hotel.name}*\n"
            f"📍 {hotel.city}, {hotel.country}\n\n"
            f"📝 *Description:*\n_{hotel.description}_\n\n"
            f"✨ *Amenities:*\n{amenities}\n\n"
            f"💰 *Price:* {format_currency(hotel.price_per_night)} per night\n"
            f"⭐ *Rating:* {hotel.rating} {hotel.star_display}"
        )

    @staticmethod
    def booking_summary(hotel: Hotel, check_in_str: str, check_out_str: str, nights: int, total_cost: float) -> str:
        return (
            "📅 *Booking Summary*\n\n"
            f"🏨 *Hotel:* {hotel.name}\n"
            f"📥 *Check-in:* {check_in_str}\n"
            f"📤 *Check-out:* {check_out_str}\n"
            f"🌙 *Duration:* {nights} night(s)\n"
            "--------------------------\n"
            f"💰 *Total Cost:* {format_currency(total_cost)}\n\n"
            "Please type 'CONFIRM' to finalize your mock booking!"
        )

    @staticmethod
    def booking_confirmation(booking: Booking, hotel_name: str) -> str:
        return (
            "✅ *Booking Confirmed!* ✅\n\n"
            f"Your stay at *{hotel_name}* has been reserved.\n\n"
            f"🎫 *Booking ID:* `{booking.booking_id}`\n"
            f"📅 *Dates:* {booking.check_in} to {booking.check_out}\n"
            f"💰 *Total Paid (Mock):* {format_currency(booking.total_cost)}\n\n"
            "Thank you for choosing our bot! Safe travels! ✈️"
        )
