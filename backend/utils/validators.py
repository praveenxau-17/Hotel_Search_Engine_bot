from datetime import datetime, date
from typing import Optional, Tuple

def validate_date(date_str: str) -> Optional[date]:
    """Validates date format YYYY-MM-DD"""
    try:
        dt = datetime.strptime(date_str, "%Y-%m-%d").date()
        # Ensure date is not in the past
        if dt < date.today():
            return None
        return dt
    except ValueError:
        return None

def validate_date_range(check_in: date, check_out: date) -> bool:
    """Ensures check-out is after check-in"""
    return check_out > check_in

def sanitize_city_input(text: str) -> str:
    """Basic sanitization for city input"""
    return text.strip().title()
