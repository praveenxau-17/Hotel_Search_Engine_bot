from dataclasses import dataclass, field
from datetime import date
from typing import Dict, List, Optional
from backend.models.hotel import Hotel

@dataclass
class UserSession:
    user_id: int
    current_city: Optional[str] = None
    search_results: List[Hotel] = field(default_factory=list)
    selected_hotel: Optional[Hotel] = None
    check_in: Optional[date] = None
    check_out: Optional[date] = None

class SessionManager:
    def __init__(self):
        self.sessions: Dict[int, UserSession] = {}

    def get_session(self, user_id: int) -> UserSession:
        if user_id not in self.sessions:
            self.sessions[user_id] = UserSession(user_id=user_id)
        return self.sessions[user_id]

    def clear_session(self, user_id: int):
        if user_id in self.sessions:
            del self.sessions[user_id]
            
    def update_session(self, user_id: int, **kwargs):
        session = self.get_session(user_id)
        for key, value in kwargs.items():
            if hasattr(session, key):
                setattr(session, key, value)
