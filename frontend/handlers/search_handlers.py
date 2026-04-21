from telegram import Update, InlineKeyboardMarkup
from telegram.ext import (
    ContextTypes,
    ConversationHandler,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    filters,
)
from frontend.messages.templates import MessageTemplates
from frontend.keyboards.inline_keyboards import (
    hotel_results_keyboard,
    hotel_detail_keyboard,
    search_again_keyboard,
)
from backend.utils.validators import sanitize_city_input

# States
ASK_CITY, SHOW_RESULTS, SHOW_DETAILS = range(3)

async def search_entry(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Entry point for /search"""
    await update.message.reply_text("🔎 Please enter the city name you want to search in (e.g., Paris, Tokyo, New York):")
    return ASK_CITY

async def handle_city_input(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """User enters city name"""
    user_id = update.effective_user.id
    city_name = sanitize_city_input(update.message.text)
    
    hotel_service = context.bot_data.get('hotel_service')
    session_manager = context.bot_data.get('session_manager')
    
    results = hotel_service.search_by_city(city_name)
    
    if not results:
        cities = hotel_service.get_available_cities()
        await update.message.reply_text(
            f"Sorry, we couldn't find any hotels in *{city_name}*.\n\nTry one of these: {', '.join(cities)}",
            parse_mode="Markdown",
            reply_markup=search_again_keyboard()
        )
        return ASK_CITY # Let them try again

    # Store results in session
    session_manager.update_session(user_id, current_city=city_name, search_results=results)
    
    await update.message.reply_text(
        f"🏨 Found {len(results)} hotels in *{city_name}*:",
        parse_mode="Markdown",
        reply_markup=hotel_results_keyboard(results)
    )
    return SHOW_RESULTS

async def hotel_selection_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """User clicks on a hotel from search results"""
    query = update.callback_query
    await query.answer()
    
    user_id = query.from_user.id
    hotel_id = query.data.split(":")[1]
    
    hotel_service = context.bot_data.get('hotel_service')
    session_manager = context.bot_data.get('session_manager')
    
    hotel = hotel_service.get_hotel_by_id(hotel_id)
    if hotel:
        session_manager.update_session(user_id, selected_hotel=hotel)
        await query.edit_message_text(
            MessageTemplates.hotel_detail(hotel),
            parse_mode="Markdown",
            reply_markup=hotel_detail_keyboard(hotel.id)
        )
        return SHOW_DETAILS
    
    return SHOW_RESULTS

async def sort_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handles sorting requests via callback"""
    query = update.callback_query
    await query.answer()
    
    user_id = query.from_user.id
    sort_type = query.data.split(":")[1]
    
    hotel_service = context.bot_data.get('hotel_service')
    session_manager = context.bot_data.get('session_manager')
    session = session_manager.get_session(user_id)
    
    results = session.search_results
    if sort_type == "price":
        results = hotel_service.sort_hotels(results, key="price")
    elif sort_type == "rating":
        results = hotel_service.sort_hotels(results, key="rating")
        
    session_manager.update_session(user_id, search_results=results)
    
    await query.edit_message_text(
        f"🏨 Found {len(results)} hotels in *{session.current_city}* (Sorted by {sort_type}):",
        parse_mode="Markdown",
        reply_markup=hotel_results_keyboard(results)
    )
    return SHOW_RESULTS

async def back_to_results(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Goes back to result list from details"""
    query = update.callback_query
    await query.answer()
    
    user_id = query.from_user.id
    session_manager = context.bot_data.get('session_manager')
    session = session_manager.get_session(user_id)
    
    await query.edit_message_text(
        f"🏨 Found {len(session.search_results)} hotels in *{session.current_city}*:",
        parse_mode="Markdown",
        reply_markup=hotel_results_keyboard(session.search_results)
    )
    return SHOW_RESULTS

def get_search_handler():
    return ConversationHandler(
        entry_points=[CommandHandler("search", search_entry)],
        states={
            ASK_CITY: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_city_input)],
            SHOW_RESULTS: [
                CallbackQueryHandler(hotel_selection_callback, pattern="^hotel_view:"),
                CallbackQueryHandler(sort_callback, pattern="^sort:"),
                CallbackQueryHandler(search_entry, pattern="^new_search")
            ],
            SHOW_DETAILS: [
                CallbackQueryHandler(back_to_results, pattern="^back_to_results")
            ]
        },
        fallbacks=[CommandHandler("cancel", lambda u, c: -1)],
        allow_reentry=True,
        per_message=False
    )
