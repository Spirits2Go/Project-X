from sqlalchemy import create_engine, select, func, and_, or_, not_
from sqlalchemy.orm import scoped_session, sessionmaker, joinedload
from pathlib import Path
from datetime import datetime

from data_access.data_base import init_db
from data_models.models import *


class HotelManager(object):
    def __init__(self, database_file):
        database_path = Path(database_file)
        if not database_path.is_file():
            init_db(database_file, generate_example_data=True)
        self.__engine = create_engine(f'sqlite:///{database_file}', echo=False)
        self.__session = scoped_session(sessionmaker(bind=self.__engine))

    def add_new_hotel(self):
        # Gather input for the new hotel
        name = input("Enter the hotel name: ")
        stars = int(input("Enter the star rating of the hotel: "))
        street = input("Enter the street address of the hotel: ")
        zip_code = input("Enter the ZIP code of the hotel: ")
        city = input("Enter the city where the hotel is located: ")

        # Create the Address instance
        address = Address(street=street, zip=zip_code, city=city)

        # Create the new hotel instance
        new_hotel = Hotel(name=name, stars=stars, address=address)

        # Add rooms
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
                price=price
            )
            new_hotel.rooms.append(room)

            more_rooms = input("Add another room? (yes/no): ").lower() == 'yes'

        print(new_hotel)
        # Add the hotel to the session and commit it
        self.__session.add(new_hotel)
        self.__session.commit()

        print(f"Added new hotel: {new_hotel.name}")

    def list_all_hotels_with_details(self):
        print("Listing all hotels with room details and bookings:")
        try:
            # Execute query with appropriate options for eager loading
            hotels = self.__session.execute(
                select(Hotel).options(
                    joinedload(Hotel.rooms).joinedload(Room.bookings),
                    joinedload(Hotel.address)
                )
            ).unique().scalars().all()  # Utilize .unique() here

            for hotel in hotels:
                print(f"\nHotel Name: {hotel.name}, Stars: {hotel.stars}, Address: {hotel.address}")
                for room in hotel.rooms:
                    print(f"  Room Number: {room.number}, Type: {room.type}, Price: ${room.price}")
                    if room.bookings:
                        for booking in room.bookings:
                            print(
                                f"    Booking ID: {booking.id}, Guest ID: {booking.guest_id}, Start Date: {booking.start_date}, End Date: {booking.end_date}")
                    else:
                        print("    No bookings")
        except Exception as e:
            print(f"Error: {e}")


    def find_hotel_by_name(self, name):
        print(f"Searching for hotel: {name}")
        hotel = self.__session.execute(
            select(Hotel)
            .where(Hotel.name == name)
            .options(joinedload(Hotel.rooms), joinedload(Hotel.address))
        ).scalar()
        if hotel:
            print(f"Found Hotel - Name: {hotel.name}, Stars: {hotel.stars}, Address: {hotel.address.city}")
            for room in hotel.rooms:
                print(f"    Room Number: {room.number}, Type: {room.type}, Price: {room.price}")
        else:
            print("Hotel not found.")
        print("End of search.\n")


if __name__ == '__main__':
    database_path = "../data/database.db"
    manager = HotelManager(database_path)

    # To add a new hotel
    #manager.add_new_hotel()

    # To list all hotels
    manager.list_all_hotels_with_details()


