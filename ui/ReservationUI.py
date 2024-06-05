import os
from datetime import datetime
from sqlalchemy import create_engine, select, and_, or_, not_
from sqlalchemy.orm import scoped_session, sessionmaker, joinedload
from pathlib import Path
from data_models.models import *
from data_access.data_base import init_db
from business.UserManager import UserManager

class ReservationUI:
    def __init__(self, db_file, user_manager):
        self.__engine = create_engine(f'sqlite:///{db_file}', echo=False)
        self.__session = scoped_session(sessionmaker(bind=self.__engine))
        database_path = Path(db_file)
        if not database_path.is_file():
            init_db(db_file, generate_example_data=True)
        self.user_manager = user_manager

    def show_reservation_menu(self):
        if not self.user_manager.get_current_user():
            print("You must log in to access the reservation menu.")
            if not self.login():
                print("Login failed. Returning to main menu.")
                return
        while True:
            self.clear()
            print("Reservation Menu")
            print("1. Create Booking")
            print("2. Update Booking")
            print("3. Delete Booking")
            print("4. View My Bookings")
            print("5. Export Booking Details")
            print("6. Back to Main Menu")

            choice = input("Enter Option (1-6): ")
            if choice == "1":
                self.create_booking()
            elif choice == "2":
                self.update_booking()
            elif choice == "3":
                self.delete_booking()
            elif choice == "4":
                self.view_bookings()
            elif choice == "5":
                self.export_booking_details()
            elif choice == "6":
                break
            else:
                print("Invalid choice, please select a valid option.")
                input("Press Enter to continue...")

    def login(self):
        username = input("Enter username: ")
        password = input("Enter password: ")
        user = self.user_manager.login(username, password)
        if user:
            print("Login successful")
            return True
        else:
            print("Login failed")
            return False

    def create_booking(self):
        user = self.user_manager.get_current_user()
        if not user:
            print("You must be logged in to create a booking.")
            return

        user_id = user.id
        hotel_name = input("Enter the hotel name: ")

        hotel = self.__session.execute(select(Hotel).where(Hotel.name == hotel_name)).scalar()
        if not hotel:
            print(f"Hotel '{hotel_name}' not found.")
            return

        rooms = self.__session.execute(select(Room).where(Room.hotel_id == hotel.id, Room.is_available == True)).scalars().all()
        if not rooms:
            print(f"No available rooms found in hotel '{hotel_name}'.")
            return

        print(f"Available rooms in '{hotel_name}':")
        for room in rooms:
            print(f"Room Number: {room.number}, Type: {room.type}, Description: {room.description}, Amenities: {room.amenities}, Price: {room.price} CHF, Max Guests: {room.max_guests}")

        room_number = input("Enter the room number: ")
        room = next((room for room in rooms if room.number == room_number), None)
        if not room:
            print(f"Room '{room_number}' not found or is not available in hotel '{hotel_name}'.")
            return

        start_date_str = input("Enter start date (YYYY-MM-DD): ")
        end_date_str = input("Enter end date (YYYY-MM-DD): ")
        guests = int(input("Enter number of guests: "))
        comment = input("Enter any comments (optional): ")

        if guests > room.max_guests:
            print(f"Room '{room_number}' in hotel '{hotel_name}' cannot accommodate {guests} guests.")
            return

        try:
            start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
            end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()
            if end_date <= start_date:
                print("End date must be after start date.")
                return

            overlapping_booking = self.__session.execute(
                select(Booking).where(
                    Booking.room_hotel_id == room.hotel_id,
                    Booking.room_number == room.number,
                    or_(
                        and_(Booking.start_date <= start_date, Booking.end_date > start_date),
                        and_(Booking.start_date < end_date, Booking.end_date >= end_date),
                        and_(Booking.start_date >= start_date, Booking.end_date <= end_date)
                    )
                )
            ).first()

            if overlapping_booking:
                print(f"Room '{room_number}' in hotel '{hotel_name}' is already booked for the selected dates.")
                return

            booking = Booking(
                guest_id=user_id,
                room_hotel_id=room.hotel_id,
                room_number=room.number,
                start_date=start_date,
                end_date=end_date,
                number_of_guests=guests,
                comment=comment
            )
            self.__session.add(booking)
            self.__session.commit()
            print(f"Booking created: {booking}")
        except ValueError as e:
            print(f"Error parsing dates: {e}")

    def update_booking(self):
        self.view_bookings()
        booking_id = int(input("Enter the booking ID to update: "))
        booking = self.__session.query(Booking).filter_by(id=booking_id).first()
        if not booking:
            print(f"Booking ID {booking_id} not found.")
            return

        print("Leave fields blank to keep current values.")
        start_date_str = input(f"Enter new start date (current: {booking.start_date}, YYYY-MM-DD): ")
        end_date_str = input(f"Enter new end date (current: {booking.end_date}, YYYY-MM-DD): ")
        guests_str = input(f"Enter new number of guests (current: {booking.number_of_guests}): ")
        comment = input(f"Enter new comment (current: {booking.comment}): ")

        if start_date_str:
            booking.start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
        if end_date_str:
            booking.end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()
        if guests_str:
            guests = int(guests_str)
            room = self.__session.query(Room).filter_by(hotel_id=booking.room_hotel_id, number=booking.room_number).first()
            if guests > room.max_guests:
                print(f"Room cannot accommodate {guests} guests.")
                return
            booking.number_of_guests = guests
        if comment:
            booking.comment = comment

        self.__session.commit()
        print(f"Booking updated: {booking}")

    def delete_booking(self):
        self.view_bookings()
        booking_id = int(input("Enter the booking ID to delete: "))
        booking = self.__session.query(Booking).filter_by(id=booking_id).first()
        if booking:
            self.__session.delete(booking)
            self.__session.commit()
            print(f"Booking ID {booking_id} deleted.")
        else:
            print(f"Booking ID {booking_id} not found.")

    def view_bookings(self):
        user = self.user_manager.get_current_user()
        if not user:
            print("You must be logged in to view your bookings.")
            return

        user_id = user.id
        bookings = self.__session.query(Booking).filter_by(guest_id=user_id).all()
        if bookings:
            for booking in bookings:
                print(f"Booking ID: {booking.id}, Hotel ID: {booking.room_hotel_id}, Room Number: {booking.room_number}, "
                      f"Start Date: {booking.start_date}, End Date: {booking.end_date}, Guests: {booking.number_of_guests}, "
                      f"Comment: {booking.comment}")
        else:
            print("You have no bookings.")

    def export_booking_details(self):
        user = self.user_manager.get_current_user()
        if not user:
            print("You must be logged in to export your bookings.")
            return

        user_id = user.id
        bookings = self.__session.query(Booking).filter_by(guest_id=user_id).all()
        if not bookings:
            print("You have no bookings to export.")
            return

        with open(f'{user.username}_bookings.txt', 'w') as file:
            for booking in bookings:
                hotel = self.__session.query(Hotel).filter_by(id=booking.room_hotel_id).first()
                room = self.__session.query(Room).filter_by(hotel_id=booking.room_hotel_id, number=booking.room_number).first()
                address = self.__session.query(Address).filter_by(id=hotel.address_id).first()
                file.write(f"Booking ID: {booking.id}\n")
                file.write(f"Hotel: {hotel.name}\n")
                file.write(f"Address: {address.street}, {address.city}, {address.zip}\n")
                file.write(f"Room Number: {room.number}\n")
                file.write(f"Room Type: {room.type}\n")
                file.write(f"Room Description: {room.description}\n")
                file.write(f"Room Amenities: {room.amenities}\n")
                file.write(f"Price per Night: {room.price}\n")
                file.write(f"Start Date: {booking.start_date}\n")
                file.write(f"End Date: {booking.end_date}\n")
                file.write(f"Guests: {booking.number_of_guests}\n")
                file.write(f"Comment: {booking.comment}\n")
                file.write("\n")
        print(f"Bookings exported to {user.username}_bookings.txt")

    @staticmethod
    def clear():
        os.system('cls' if os.name == 'nt' else 'clear')
