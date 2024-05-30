import os
from datetime import datetime
from sqlalchemy import create_engine, select, and_, or_, not_
from sqlalchemy.orm import scoped_session, sessionmaker
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
            print("5. Back to Main Menu")

            choice = input("Enter Option (1-5): ")
            if choice == "1":
                self.create_booking()
            elif choice == "2":
                self.update_booking()
            elif choice == "3":
                self.delete_booking()
            elif choice == "4":
                self.view_bookings()
            elif choice == "5":
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
        room_id = int(input("Enter the room ID: "))
        start_date_str = input("Enter start date (YYYY-MM-DD): ")
        end_date_str = input("Enter end date (YYYY-MM-DD): ")
        guests = int(input("Enter number of guests: "))
        comment = input("Enter any comments (optional): ")

        try:
            start_date = datetime.strptime(start_date_str, '%Y-%m-%d').date()
            end_date = datetime.strptime(end_date_str, '%Y-%m-%d').date()
            booking = Booking(
                guest_id=user_id,
                room_hotel_id=room_id,
                room_number=room_id,
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
        booking_id = int(input("Enter the booking ID to update: "))
        comment = input("Enter new comment: ")
        booking = self.__session.query(Booking).filter_by(id=booking_id).first()
        if booking:
            booking.comment = comment
            self.__session.commit()
            print(f"Booking updated: {booking}")
        else:
            print(f"Booking ID {booking_id} not found.")

    def delete_booking(self):
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
                print(f"Booking ID: {booking.id}, Room ID: {booking.room_hotel_id}, Room Number: {booking.room_number}, "
                      f"Start Date: {booking.start_date}, End Date: {booking.end_date}, Guests: {booking.number_of_guests}, "
                      f"Comment: {booking.comment}")
        else:
            print("You have no bookings.")

    @staticmethod
    def clear():
        os.system('cls' if os.name == 'nt' else 'clear')