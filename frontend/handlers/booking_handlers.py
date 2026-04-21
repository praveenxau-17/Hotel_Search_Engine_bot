from telegram import Update
from telegram.ext import (
    ContextTypes,
    ConversationHandler,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    filters,
)
from frontend.messages.templates import MessageTemplates
from frontend.keyboards.inline_keyboards import confirm_booking_keyboard
from backend.utils.validators import validate_date, validate_date_range

# States
ASK_DATES, CONFIRM_BOOKING = range(2)

async def booking_entry(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Triggered by 'Book Now' button. Starts booking flow."""
    query = update.callback_query
    await query.answer()
    
    # We already have the hotel selected in the session
    await query.message.reply_text(
        "📅 *How many nights would you like to stay?*\n\n"
        "Please enter your dates in the format: `YYYY-MM-DD to YYYY-MM-DD`\n"
        "Example: `2024-12-01 to 2024-12-05`",
        parse_mode="Markdown"
    )
    return ASK_DATES

async def handle_dates_input(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """User enters dates like YYYY-MM-DD to YYYY-MM-DD"""
    user_id = update.effective_user.id
    input_text = update.message.text
    
    session_manager = context.bot_data.get('session_manager')
    booking_service = context.bot_data.get('booking_service')
    session = session_manager.get_session(user_id)
    
    try:
        parts = input_text.lower().split(" to ")
        if len(parts) != 2:
            raise ValueError("Invalid format")
            
        check_in = validate_date(parts[0].strip())
        check_out = validate_date(parts[1].strip())
        
        if not check_in or not check_out:
            raise ValueError("Invalid date format or date is in the past")
            
        if not validate_date_range(check_in, check_out):
            raise ValueError("Check-out must be after check-in")
            
        nights = (check_out - check_in).days
        total_cost = session.selected_hotel.price_per_night * nights
        
        session_manager.update_session(user_id, check_in=check_in, check_out=check_out)
        
        await update.message.reply_text(
            MessageTemplates.booking_summary(
                session.selected_hotel, 
                str(check_in), 
                str(check_out), 
                nights, 
                total_cost
            ),
            parse_mode="Markdown"
        )
        return CONFIRM_BOOKING
        
    except ValueError as e:
        await update.message.reply_text(f"❌ Error: {str(e)}. Please try again with format `YYYY-MM-DD to YYYY-MM-DD`.")
        return ASK_DATES

async def confirm_booking(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """User types CONFIRM or clicks confirm"""
    user_id = update.effective_user.id
    text = update.message.text.strip().upper()
    
    if text != "CONFIRM":
        await update.message.reply_text("Please type 'CONFIRM' to finalize, or /cancel to stop.")
        return CONFIRM_BOOKING
        
    session_manager = context.bot_data.get('session_manager')
    booking_service = context.bot_data.get('booking_service')
    session = session_manager.get_session(user_id)
    
    booking = booking_service.create_booking(
        user_id, 
        session.selected_hotel, 
        session.check_in, 
        session.check_out
    )
    
    await update.message.reply_text(
        MessageTemplates.booking_confirmation(booking, session.selected_hotel.name),
        parse_mode="Markdown"
    )
    
    # Clear session after successful booking
    session_manager.clear_session(user_id)
    return ConversationHandler.END

async def cancel_booking_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    await query.edit_message_text("❌ Booking cancelled.")
    return ConversationHandler.END

def get_booking_handler():
    return ConversationHandler(
        entry_points=[CallbackQueryHandler(booking_entry, pattern="^book_start:")],
        states={
            ASK_DATES: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_dates_input)],
            # Simplified: just wait for the word CONFIRM
            CONFIRM_BOOKING: [MessageHandler(filters.TEXT & ~filters.COMMAND, confirm_booking)]
        },
        fallbacks=[CommandHandler("cancel", lambda u, c: ConversationHandler.END)],
        allow_reentry=True,
        per_message=False
    )
