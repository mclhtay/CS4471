from HotelBooking.Models.room import Room

rooms = Room().get_available_rooms()
print(rooms)
