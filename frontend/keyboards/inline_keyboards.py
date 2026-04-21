from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from backend.models.hotel import Hotel
from typing import List

def hotel_results_keyboard(hotels: List[Hotel]) -> InlineKeyboardMarkup:
    keyboard = []
    for hotel in hotels:
        keyboard.append([InlineKeyboardButton(f"{hotel.name} - ${hotel.price_per_night}", callback_data=f"hotel_view:{hotel.id}")])
    
    # Navigation/Sort options
    keyboard.append([
        InlineKeyboardButton("💲 Sort by Price", callback_data="sort:price"),
        InlineKeyboardButton("⭐ Sort by Rating", callback_data="sort:rating")
    ])
    keyboard.append([InlineKeyboardButton("🔍 New Search", callback_data="new_search")])
    
    return InlineKeyboardMarkup(keyboard)

def hotel_detail_keyboard(hotel_id: str) -> InlineKeyboardMarkup:
    keyboard = [
        [InlineKeyboardButton("📅 Book Now", callback_data=f"book_start:{hotel_id}")],
        [InlineKeyboardButton("🔙 Back to Results", callback_data="back_to_results")]
    ]
    return InlineKeyboardMarkup(keyboard)

def sort_keyboard() -> InlineKeyboardMarkup:
    keyboard = [
        [InlineKeyboardButton("Price: Low to High", callback_data="sort:price_asc")],
        [InlineKeyboardButton("Price: High to Low", callback_data="sort:price_desc")],
        [InlineKeyboardButton("Rating: High to Low", callback_data="sort:rating_desc")]
    ]
    return InlineKeyboardMarkup(keyboard)

def confirm_booking_keyboard() -> InlineKeyboardMarkup:
    keyboard = [
        [InlineKeyboardButton("✅ Confirm Booking", callback_data="confirm_final")],
        [InlineKeyboardButton("❌ Cancel", callback_data="cancel_booking")]
    ]
    return InlineKeyboardMarkup(keyboard)

def search_again_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup([[InlineKeyboardButton("🔍 Search Again", callback_data="new_search")]])

def cities_keyboard(cities: List[str]) -> InlineKeyboardMarkup:
    keyboard = []
    row = []
    for i, city in enumerate(cities):
        row.append(InlineKeyboardButton(city, callback_data=f"city_select:{city}"))
        if (i + 1) % 2 == 0:
            keyboard.append(row)
            row = []
    if row:
        keyboard.append(row)
    return InlineKeyboardMarkup(keyboard)
