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
            print("5. Update Room Information")
            print("6. Edit Bookings")
            print("7. Back to Main Menu")

            choice = input("Enter Option (1-7): ")
            if choice == "1":
                self.add_new_hotel()
            elif choice == "2":
                self.list_all_hotels_with_details()
            elif choice == "3":
                self.find_hotel_by_name()
            elif choice == "4":
                self.update_hotel_information()
            elif choice == "5":
                self.update_room_information()
            elif choice == "6":
                self.edit_bookings()
            elif choice == "7":
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

    def update_room_information(self):
        hotel_name = input("Enter the hotel name: ")
        hotel = self.__session.execute(
            select(Hotel).where(Hotel.name == hotel_name).options(joinedload(Hotel.rooms))
        ).scalar()

        if not hotel:
            print("Hotel not found.")
            return

        while True:
            print(f"Updating room information for hotel: {hotel.name}")
            for room in hotel.rooms:
                print(f"Room Number: {room.number}, Type: {room.type}, Price: {room.price}, Availability: {room.is_available}")
            room_number = input("Enter the room number to update: ")
            room = next((r for r in hotel.rooms if r.number == room_number), None)

            if not room:
                print("Room not found.")
            else:
                print(f"Updating information for room {room.number}")
                room.type = input(f"Enter new room type (current: {room.type}): ") or room.type
                room.max_guests = input(f"Enter new max guests (current: {room.max_guests}): ") or room.max_guests
                room.description = input(f"Enter new description (current: {room.description}): ") or room.description
                room.amenities = input(f"Enter new amenities (current: {room.amenities}): ") or room.amenities
                room.price = input(f"Enter new price (current: {room.price}): ") or room.price
                room.is_available = input(f"Is the room available? (current: {room.is_available}) [yes/no]: ").lower() in ['yes', 'y']

                self.__session.commit()
                print(f"Room {room.number} information updated successfully.")

            more_rooms = input("Do you want to update another room? (yes/no): ").lower() == 'yes'
            if not more_rooms:
                break

    def edit_bookings(self):
        print("Listing all bookings:")
        try:
            bookings = self.__session.execute(
                select(Booking)
                .options(
                    joinedload(Booking.guest),
                    joinedload(Booking.room).joinedload(Room.hotel)
                )
            ).unique().scalars().all()

            for booking in bookings:
                guest_info = "Guest not found"
                if booking.guest:
                    guest_info = f"{booking.guest.firstname} {booking.guest.lastname}"
                print(f"Booking ID: {booking.id}, Hotel: {booking.room.hotel.name}, Room Number: {booking.room.number}, "
                      f"Guest: {guest_info}, Start Date: {booking.start_date}, "
                      f"End Date: {booking.end_date}, Phone Number: {booking.phone_number}")

            booking_id = int(input("Enter the booking ID to edit: "))
            booking = self.__session.query(Booking).filter_by(id=booking_id).first()

            if not booking:
                print("Booking not found.")
                return

            print("Leave fields blank to keep current values.")
            start_date_str = input(f"Enter new start date (current: {booking.start_date}, YYYY-MM-DD): ")
            end_date_str = input(f"Enter new end date (current: {booking.end_date}, YYYY-MM-DD): ")
            guests_str = input(f"Enter new number of guests (current: {booking.number_of_guests}): ")
            phone_number = input(f"Enter new phone number (current: {booking.phone_number}): ")
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
            if phone_number:
                booking.phone_number = phone_number
            if comment:
                booking.comment = comment

            self.__session.commit()
            print(f"Booking updated: {booking}")

        except Exception as e:
            print(f"Error: {e}")


    @staticmethod
    def clear():
        os.system('cls' if os.name == 'nt' else 'clear')
