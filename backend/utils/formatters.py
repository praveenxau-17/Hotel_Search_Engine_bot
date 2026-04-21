from typing import List

def format_price_indicator(price_per_night: float) -> str:
    if price_per_night < 150:
        return "$"
    elif price_per_night < 300:
        return "$$"
    else:
        return "$$$"

def format_star_rating(rating: float) -> str:
    rounded = int(round(rating))
    return "⭐" * rounded

def format_amenities(amenities: List[str]) -> str:
    # Map common amenities to emojis
    emoji_map = {
        "WiFi": "📶",
        "Pool": "🏊",
        "Gym": "🏋️",
        "Restaurant": "🍴",
        "Spa": "🧴",
        "Breakfast": "🍳",
        "Parking": "🚗"
    }
    formatted = []
    for am in amenities:
        emoji = emoji_map.get(am, "🔹")
        formatted.append(f"{emoji} {am}")
    return "\n".join(formatted)

def format_currency(amount: float, currency: str = "USD") -> str:
    if currency == "USD":
        return f"${amount:,.2f}"
    return f"{amount:,.2f} {currency}"
