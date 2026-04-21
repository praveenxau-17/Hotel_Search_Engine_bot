from telegram import Update
from telegram.ext import ContextTypes
from frontend.messages.templates import MessageTemplates
from backend.services.hotel_service import HotelService

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handles /start command"""
    await update.message.reply_text(
        MessageTemplates.welcome_message(),
        parse_mode="Markdown"
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handles /help command"""
    await update.message.reply_text(
        MessageTemplates.help_message(),
        parse_mode="Markdown"
    )

async def cities_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handles /cities command"""
    hotel_service = context.bot_data.get('hotel_service')
    if hotel_service:
        cities = hotel_service.get_available_cities()
        await update.message.reply_text(
            MessageTemplates.city_list_message(cities),
            parse_mode="Markdown"
        )
    else:
        await update.message.reply_text("Error: Hotel service not available.")

async def cancel_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handles /cancel command and ends transitions"""
    session_manager = context.bot_data.get('session_manager')
    if update.message:
        user_id = update.message.from_user.id
        if session_manager:
            session_manager.clear_session(user_id)
        await update.message.reply_text("❌ Operation cancelled. Session cleared.")
    return -1 # END CONVERSATION
