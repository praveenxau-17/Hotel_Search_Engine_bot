import json
import os
import requests
from typing import List, Optional, Set
from backend.models.hotel import Hotel

class HotelService:
    # Use the mock API provided by the user
    API_BASE_URL = "https://69e73bbe68208c1debe8820a.mockapi.io/api/hotels"
    
    def __init__(self, data_path: str = "backend/data/hotel_data.json"):
        self.data_path = data_path
        self.hotels: List[Hotel] = []
        self._load_hotels()

    def _load_hotels(self):
        # Try fetching from API first
        try:
            response = requests.get(self.API_BASE_URL, timeout=10)
            if response.status_code == 200:
                data = response.json()
                self.hotels = [Hotel.from_dict(item) for item in data]
                print(f"✅ Successfully loaded {len(self.hotels)} hotels from Mock API.")
                return
        except Exception as e:
            print(f"⚠️ API Fetch failed ({e}). Falling back to local data.")

        # Fallback to local JSON if API fails or isn't available
        if os.path.exists(self.data_path):
            try:
                with open(self.data_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.hotels = [Hotel.from_dict(item) for item in data]
                    print(f"✅ Loaded {len(self.hotels)} hotels from local fallback.")
            except Exception as e:
                print(f"❌ Failed to load local data: {e}")

    def search_by_city(self, city: str) -> List[Hotel]:
        city = city.strip().lower()
        return [h for h in self.hotels if h.city.lower() == city]

    def get_hotel_by_id(self, hotel_id: str) -> Optional[Hotel]:
        for h in self.hotels:
            if h.id == hotel_id:
                return h
        return None

    def get_available_cities(self) -> List[str]:
        cities = {h.city for h in self.hotels}
        return sorted(list(cities))

    def sort_hotels(self, hotels: List[Hotel], key: str = "price", ascending: bool = True) -> List[Hotel]:
        if key == "price":
            return sorted(hotels, key=lambda x: x.price_per_night, reverse=not ascending)
        elif key == "rating":
            return sorted(hotels, key=lambda x: x.rating, reverse=not ascending)
        return hotels

    def filter_by_price_range(self, hotels: List[Hotel], min_price: float, max_price: float) -> List[Hotel]:
        return [h for h in hotels if min_price <= h.price_per_night <= max_price]
