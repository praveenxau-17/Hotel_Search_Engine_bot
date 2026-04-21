from dataclasses import dataclass
from typing import List, Dict, Any

@dataclass
class Hotel:
    id: str
    name: str
    city: str
    country: str
    price_per_night: float
    currency: str
    rating: float
    amenities: List[str]
    description: str
    image_emoji: str

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Hotel':
        return cls(
            id=data['id'],
            name=data['name'],
            city=data['city'],
            country=data['country'],
            price_per_night=data['price_per_night'],
            currency=data['currency'],
            rating=data['rating'],
            amenities=data['amenities'],
            description=data['description'],
            image_emoji=data['image_emoji']
        )

    @property
    def price_indicator(self) -> str:
        if self.price_per_night < 150:
            return "$"
        elif self.price_per_night < 300:
            return "$$"
        else:
            return "$$$"

    @property
    def star_display(self) -> str:
        rounded_rating = int(round(self.rating))
        return "⭐" * rounded_rating
