from datetime import date
from typing import Dict
from backend.models.booking import Booking, generate_booking_id
from backend.models.hotel import Hotel

class BookingService:
    def __init__(self):
        # In-memory storage for bookings (keyed by booking_id for easy lookup)
        self.bookings: Dict[str, Booking] = {}

    def create_booking(self, user_id: int, hotel: Hotel, check_in: date, check_out: date) -> Booking:
        nights = (check_out - check_in).days
        total_cost = hotel.price_per_night * nights
        booking_id = generate_booking_id()
        
        booking = Booking(
            booking_id=booking_id,
            hotel_id=hotel.id,
            user_id=user_id,
            check_in=check_in,
            check_out=check_out,
            nights=nights,
            total_cost=total_cost,
            currency=hotel.currency
        )
        
        self.bookings[booking_id] = booking
        return booking

    def get_booking(self, booking_id: str) -> Booking:
        return self.bookings.get(booking_id)
