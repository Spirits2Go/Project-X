from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from data_models.models import Login, Guest, Booking, Room, RegisteredGuest

class UserManager:
    def __init__(self, db_path):
        self.__engine = create_engine(f"sqlite:///{db_path}")
        self.__Session = sessionmaker(bind=self.__engine)
        self.__session = self.__Session()

    def login(self, username, password):
        user = self.__session.query(Login).filter_by(username=username, password=password).first()
        if user:
            print("Login successful")
            return user
        else:
            print("Login failed")
            return None

    def get_booking_history(self, user_id):
        guest = self.__session.query(Guest).filter_by(id=user_id).first()
        if guest:
            bookings = self.__session.query(Booking).filter_by(guest_id=guest.id).all()
            for booking in bookings:
                print(booking)
        else:
            print("User not found")

    def create_booking(self, user_id, room_hotel_id, room_number, start_date, end_date, number_of_guests, comment):
        room = self.__session.query(Room).filter_by(hotel_id=room_hotel_id, number=room_number).first()
        if room:
            booking = Booking(
                guest_id=user_id,
                room_hotel_id=room_hotel_id,
                room_number=room_number,
                start_date=start_date,
                end_date=end_date,
                number_of_guests=number_of_guests,
                comment=comment
            )
            self.__session.add(booking)
            self.__session.commit()
            print("Booking created:", booking)
        else:
            print("Room not found")

    def update_booking(self, booking_id, comment):
        booking = self.__session.query(Booking).filter_by(id=booking_id).first()
        if booking:
            booking.comment = comment
            self.__session.commit()
            print("Booking updated:", booking)
        else:
            print("Booking not found")

    def delete_booking(self, booking_id):
        booking = self.__session.query(Booking).filter_by(id=booking_id).first()
        if booking:
            self.__session.delete(booking)
            self.__session.commit()
            print("Booking deleted")
        else:
            print("Booking not found")
