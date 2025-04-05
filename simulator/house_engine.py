class HouseEngine:
    """Responsible for managing room definitions and current status per tick."""

    def __init__(self):
        self.rooms = self._init_rooms()

    def _init_rooms(self):
        """Initializes a dictionary of rooms with default inactive state."""
        room_names = [
            "LivingRoom",
            "Kitchen",
            "Balcony",
            "ParentsRoom",
            "KobeRoom",
            "GavriellaRoom",
            "Bathroom1",
            "Bathroom2",
        ]
        return {room: {"active": False} for room in room_names}

    def update_room_status(self, occupants):
        """Marks rooms as active based on current occupant locations."""
        active_rooms = set(o["location"] for o in occupants if o.get("location"))
        for room in self.rooms:
            self.rooms[room]["active"] = room in active_rooms

    def get_active_rooms(self):
        """Returns a list of currently active rooms."""
        return [room for room, data in self.rooms.items() if data["active"]]

    def get_room_state(self):
        """Returns the entire room state dictionary."""
        return self.rooms
