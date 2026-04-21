import os
from dotenv import load_dotenv
from telegram.ext import ApplicationBuilder, CommandHandler
from frontend.handlers.command_handlers import start_command, help_command, cities_command, cancel_command
from frontend.handlers.search_handlers import get_search_handler
from frontend.handlers.booking_handlers import get_booking_handler
from backend.services.hotel_service import HotelService
from backend.services.booking_service import BookingService
from backend.services.session_service import SessionManager

# Load environment variables
load_dotenv(dotenv_path="backend/.env")

def create_application():
    token = os.getenv("BOT_TOKEN")
    if not token or token == "YOUR_TELEGRAM_BOT_TOKEN_HERE":
        print("⚠️ Warning: BOT_TOKEN not set correctly in backend/.env")
        return None

    application = ApplicationBuilder().token(token).build()

    # Initialize services
    hotel_service = HotelService()
    booking_service = BookingService()
    session_manager = SessionManager()

    # Store services in bot_data for access in handlers
    application.bot_data['hotel_service'] = hotel_service
    application.bot_data['booking_service'] = booking_service
    application.bot_data['session_manager'] = session_manager

    # Register Command Handlers
    application.add_handler(CommandHandler("start", start_command))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("cities", cities_command))
    application.add_handler(CommandHandler("cancel", cancel_command))

    # Register Conversation Handlers
    application.add_handler(get_search_handler())
    application.add_handler(get_booking_handler())

    return application

if __name__ == "__main__":
    app = create_application()
    if app:
        print("🤖 Bot is starting...")
        app.run_polling()
