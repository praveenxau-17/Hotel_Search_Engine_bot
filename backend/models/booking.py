import random
import string
from dataclasses import dataclass
from datetime import date

def generate_booking_id() -> str:
    """Generates a random booking ID like #HOTEL-123456"""
    digits = ''.join(random.choices(string.digits, k=6))
    return f"#HOTEL-{digits}"

@dataclass
class Booking:
    booking_id: str
    hotel_id: str
    user_id: int
    check_in: date
    check_out: date
    nights: int
    total_cost: float
    currency: str
