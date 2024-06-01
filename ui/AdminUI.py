import os
from sqlalchemy import create_engine, select
from sqlalchemy.orm import scoped_session, sessionmaker, joinedload
from pathlib import Path
from data_access.data_base import init_db
from data_models.models import *
from business.UserManager import UserManager

class AdminUI:
    def __init__(self, database_file, user_manager):
        database_path = Path(database_file)
        if not database_path.is_file():
            init_db(database_file, generate_example_data=True)
        self.__engine = create_engine(f'sqlite:///{database_file}', echo=False)
        self.__session = scoped_session(sessionmaker(bind=self.__engine))
        self.user_manager = user_manager

    def show_admin_menu(self):
        if not self.user_manager.get_current_user():
            print("You must log in to access the admin menu.")
            self.login()

        while True:
            self.clear()
            print("Admin Menu")
            print("1. Add New Hotel")
            print("2. List All Hotels with Details")
            print("3. Find Hotel by Name")
            print("4. Update Hotel Information")
            print("5. Update Room Availability")
            print("6. Update Room Prices")
            print("7. Update User Bookings")
            print("8. Back to Main Menu")

            choice = input("Enter Option (1-8): ")
            if choice == "1":
                self.add_new_hotel()
            elif choice == "2":
                self.list_all_hotels_with_details()
            elif choice == "3":
                self.find_hotel_by_name()
            elif choice == "4":
                self.update_hotel_information()
            elif choice == "5":
                self.update_room_availability()
            elif choice == "6":
                self.update_room_prices()
            elif choice == "7":
                self.update_user_bookings()
            elif choice == "8":
                break
            else:
                print("Invalid choice, please select a valid option.")

    def login(self):
        username = input("Enter username: ")
        password = input("Enter password: ")
        if not self.user_manager.login(username, password):
            print("Login failed. Returning to main menu.")
            return

    def add_new_hotel(self):
        name = input("Enter the hotel name: ")
        stars = int(input("Enter the star rating of the hotel: "))
        street = input("Enter the street address of the hotel: ")
        zip_code = input("Enter the ZIP code of the hotel: ")
        city = input("Enter the city where the hotel is located: ")

        address = Address(street=street, zip=zip_code, city=city)
        new_hotel = Hotel(name=name, stars=stars, address=address)

        more_rooms = True
        while more_rooms:
            room_number = input("Enter room number: ")
            room_type = input("Enter room type (e.g., double room, single room): ")
            max_guests = int(input("Enter maximum number of guests for the room: "))
            description = input("Enter a description for the room: ")
            amenities = input("Enter amenities for the room (comma separated): ")
            price = float(input("Enter price per night for the room: "))

            room = Room(
                number=room_number,
                type=room_type,
                max_guests=max_guests,
                description=description,
                amenities=amenities,
                price=price,
                is_available=True  # Default to available
            )
            new_hotel.rooms.append(room)

            more_rooms = input("Add another room? (yes/no): ").lower() == 'yes'

        self.__session.add(new_hotel)
        self.__session.commit()

        print(f"Added new hotel: {new_hotel.name}")

    def list_all_hotels_with_details(self):
        print("Listing all hotels with room details and bookings:")
        try:
            hotels = self.__session.execute(
                select(Hotel).options(
                    joinedload(Hotel.rooms).joinedload(Room.bookings),
                    joinedload(Hotel.address)
                )
            ).unique().scalars().all()

            for hotel in hotels:
                print(f"\nHotel Name: {hotel.name}, Stars: {hotel.stars}, Address: {hotel.address}")
                for room in hotel.rooms:
                    print(f"Room Number: {room.number}, Type: {room.type}, Price: {room.price}, Availability: {room.is_available}")
                    if room.bookings:
                        for booking in room.bookings:
                            print(f"Booking ID: {booking.id}, Guest ID: {booking.guest_id}, Start Date: {booking.start_date}, End Date: {booking.end_date}")
                    else:
                        print("No bookings")
        except Exception as e:
            print(f"Error: {e}")

    def find_hotel_by_name(self):
        name = input("Enter the hotel name to search: ")
        hotel = self.__session.execute(
            select(Hotel)
            .where(Hotel.name == name)
            .options(joinedload(Hotel.rooms), joinedload(Hotel.address))
        ).scalar()
        if hotel:
            print(f"Found Hotel - Name: {hotel.name}, Stars: {hotel.stars}, Address: {hotel.address.city}")
            for room in hotel.rooms:
                print(f"Room Number: {room.number}, Type: {room.type}, Price: {room.price}, Availability: {room.is_available}")
        else:
            print("Hotel not found.")

    def update_hotel_information(self):
        name = input("Enter the hotel name to update: ")
        hotel = self.__session.execute(
            select(Hotel).where(Hotel.name == name).options(joinedload(Hotel.address))
        ).scalar()

        if not hotel:
            print("Hotel not found.")
            return

        print(f"Updating information for hotel: {hotel.name}")
        new_name = input(f"Enter new name (current: {hotel.name}): ") or hotel.name
        new_stars = input(f"Enter new star rating (current: {hotel.stars}): ")
        new_stars = int(new_stars) if new_stars else hotel.stars

        address = hotel.address
        new_street = input(f"Enter new street (current: {address.street}): ") or address.street
        new_zip = input(f"Enter new ZIP code (current: {address.zip}): ") or address.zip
        new_city = input(f"Enter new city (current: {address.city}): ") or address.city

        hotel.name = new_name
        hotel.stars = new_stars
        address.street = new_street
        address.zip = new_zip
        address.city = new_city

        self.__session.commit()
        print("Hotel information updated successfully.")

    def update_room_availability(self):
        hotel_name = input("Enter the hotel name: ")
        hotel = self.__session.execute(
            select(Hotel).where(Hotel.name == hotel_name).options(joinedload(Hotel.rooms))
        ).scalar()

        if not hotel:
            print("Hotel not found.")
            return

        print(f"Updating room availability for hotel: {hotel.name}")
        for room in hotel.rooms:
            print(f"Room Number: {room.number}, Type: {room.type}, Current Availability: {room.is_available}")
            is_available = input(f"Is room {room.number} available? (yes/no): ").strip().lower() == 'yes'
            room.is_available = is_available

        self.__session.commit()
        print("Room availability updated successfully.")

    def update_room_prices(self):
        hotel_name = input("Enter the hotel name: ")
        hotel = self.__session.execute(
            select(Hotel).where(Hotel.name == hotel_name).options(joinedload(Hotel.rooms))
        ).scalar()

        if not hotel:
            print("Hotel not found.")
            return

        print(f"Updating room prices for hotel: {hotel.name}")
        for room in hotel.rooms:
            print(f"Room Number: {room.number}, Type: {room.type}, Current Price: {room.price}")
            new_price = input(f"Enter new price for room {room.number} (current: {room.price}): ")
            if new_price:
                room.price = float(new_price)

        self.__session.commit()
        print("Room prices updated successfully.")

    def update_user_bookings(self):
        hotel_name = input("Enter the hotel name: ")
        hotel = self.__session.execute(
            select(Hotel).where(Hotel.name == hotel_name).options(joinedload(Hotel.rooms).joinedload(Room.bookings))
        ).scalar()

        if not hotel:
            print("Hotel not found.")
            return

        print(f"Updating bookings for hotel: {hotel.name}")
        for room in hotel.rooms:
            for booking in room.bookings:
                print(f"Booking ID: {booking.id}, Guest ID: {booking.guest_id}, Room Number: {room.number}, "
                      f"Start Date: {booking.start_date}, End Date: {booking.end_date}, Guests: {booking.number_of_guests}, "
                      f"Comment: {booking.comment}")
                print("Leave fields blank to keep current values.")
                new_start_date = input(f"Enter new start date (current: {booking.start_date}, YYYY-MM-DD): ") or booking.start_date
                new_end_date = input(f"Enter new end date (current: {booking.end_date}, YYYY-MM-DD): ") or booking.end_date
                new_number_of_guests = input(f"Enter new number of guests (current: {booking.number_of_guests}): ")
                new_number_of_guests = int(new_number_of_guests) if new_number_of_guests else booking.number_of_guests
                new_comment = input(f"Enter new comment (current: {booking.comment}): ") or booking.comment

                if new_number_of_guests > room.max_guests:
                    print(f"Cannot update booking {booking.id}: number of guests exceeds room capacity.")
                    continue

                booking.start_date = new_start_date
                booking.end_date = new_end_date
                booking.number_of_guests = new_number_of_guests
                booking.comment = new_comment

        self.__session.commit()
        print("Bookings updated successfully.")

    @staticmethod
    def clear():
        os.system('cls' if os.name == 'nt' else 'clear')
