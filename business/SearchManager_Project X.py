from sqlalchemy import create_engine, select, func, and_, or_, not_
from sqlalchemy.orm import scoped_session, sessionmaker, joinedload
from pathlib import Path
from datetime import datetime

from data_access.data_base import init_db
from data_models.models import *


class SearchManager(object):
    def __init__(self, database_file):
        database_path = Path(database_file)
        if not database_path.is_file():
            init_db(database_file, generate_example_data=True)
        self.__engine = create_engine(f'sqlite:///{database_file}', echo=False)
        self.__session = scoped_session(sessionmaker(bind=self.__engine))

    def get_hotels_by_name(self, name):
        query = select(Hotel).where(Hotel.name.like(f"%{name}%"))
        return self.__session.execute(query).scalars().all()

    def filter_hotels_by_location(self, location):
        if not location:
            return self.__session.execute(select(Hotel)).scalars().all()
        query = select(Hotel).join(Hotel.address).where(func.lower(Address.city) == location)
        return self.__session.execute(query).scalars().all()

    def get_available_rooms(self, check_in_date, check_out_date):
        # Find rooms where no booking intersects the requested range
        query = select(Room).join(Hotel).outerjoin(Booking, and_(
            Room.hotel_id == Booking.room_hotel_id,
            Room.number == Booking.room_number
        )).filter(
            or_(
                Booking.id == None,  # No booking for the room
                not_(  # No overlapping booking
                    and_(
                        Booking.start_date < check_out_date,
                        Booking.end_date > check_in_date
                    )
                )
            )
        ).options(joinedload(Room.bookings), joinedload(Room.hotel)).distinct()

        available_rooms = self.__session.execute(query).unique().scalars().all()
        return available_rooms

    def calculate_total_price(self, price_per_night, duration):
        total_price = price_per_night * duration
        return round(total_price * 20) / 20     # Rounding to the nearest 0.05 CHF



    def filter_hotels_by_guests(self, hotels, guests):
        filtered_hotels = []
        for hotel in hotels:
            matching_rooms = [room for room in hotel.rooms if room.max_guests >= guests]
            if matching_rooms:
                # Create a new hotel dict including only matching rooms
                filtered_hotels.append(hotel)  # Add hotel with all its details if needed
        return filtered_hotels

    def filter_hotels_by_max_price(self, max_price):
        query = select(Room).join(Hotel).where(Room.price <= max_price).options(joinedload(Room.hotel))
        rooms = self.__session.execute(query).scalars().all()
        return rooms

    def filter_hotels_by_minimum_stars(self, min_stars):
        query = select(Hotel).where(Hotel.stars >= min_stars)
        return self.__session.execute(query).scalars().all()



class UserInterface(object):
    def __init__(self, search_manager):
        self.search_manager = search_manager

    def ask_for_location(self):
        location = input("Enter preferred location (press Enter to skip): ").strip()
        matching_hotels = self.search_manager.filter_hotels_by_location(location)
        if not matching_hotels:
            print("There aren't any hotels in your preferred location.")
            return
        for hotel in matching_hotels:
            print(f"Hotel: {hotel.name}, Location: {hotel.address.city}")

    def check_for_booking_date(self):
        try:
            # Asking for dates in DD.MM.YYYY format
            check_in_date_str = input("Enter your check-in date (DD.MM.YYYY): ")
            check_out_date_str = input("Enter your check-out date (DD.MM.YYYY): ")

            # Converting input dates from DD.MM.YYYY to datetime.date objects
            check_in_date = datetime.strptime(check_in_date_str, '%d.%m.%Y').date()
            check_out_date = datetime.strptime(check_out_date_str, '%d.%m.%Y').date()

            # Validation to ensure check-out is after check-in
            if check_out_date <= check_in_date:
                print("Check-out date must be after check-in date.")
                return

            # Calculating duration of stay
            duration = (check_out_date - check_in_date).days
            available_rooms = self.search_manager.get_available_rooms(check_in_date, check_out_date)

            if not available_rooms:
                print("No rooms available for the selected dates.")
            else:
                print("Available rooms:")
                for room in available_rooms:
                    total_price = self.search_manager.calculate_total_price(room.price, duration)
                    print(
                        f"Room Number: {room.number}, Type: {room.type}, Price per Night: {room.price} CHF, Total Cost for {duration} Nights: {total_price} CHF in Hotel: {room.hotel.name}, Location: {room.hotel.address.city}")
        except ValueError as e:
            print(f"Error parsing dates, please use the format DD.MM.YYYY: {e}")


    def ask_for_number_of_guests(self):
        # First, retrieve all hotels
        matching_hotels = self.search_manager.get_hotels_by_name(
            '')  # Assuming this returns all hotels when an empty string is passed
        guests = input("Enter the number of guests (press Enter to skip): ").strip()
        if guests:
            try:
                guests = int(guests)
                matching_hotels = self.search_manager.filter_hotels_by_guests(matching_hotels, guests)
                if not matching_hotels:
                    print("No hotels found that can accommodate the number of guests specified.")
                    return
            except ValueError:
                print("Invalid input. Please enter a valid number for the number of guests.")
                return

        if not matching_hotels:
            print("There aren't any matching hotels available.")
        else:
            for hotel in matching_hotels:
                print(f"Hotel: {hotel.name}, Location: {hotel.address.city}")
                for room in hotel.rooms:
                    print(f"    Room Number: {room.number}, Capacity: {room.max_guests}")

    def ask_for_maximum_price(self):
        try:
            max_price_input = input("Enter maximum price per room per night (press Enter to skip): ").strip()
            if max_price_input:
                max_price = float(max_price_input)
                rooms_under_price = self.search_manager.filter_hotels_by_max_price(max_price)
                if not rooms_under_price:
                    print("No rooms found under the price limit provided.")
                else:
                    for room in rooms_under_price:
                        print(f"Room Number: {room.number}, Type: {room.type}, Price: ${room.price} in Hotel: {room.hotel.name}, Location: {room.hotel.address.city}")
            else:
                print("No maximum price entered.")
        except ValueError:
            print("Invalid input. Please enter a valid number for the price.")

    def ask_for_minimum_stars(self):
        attempts_stars = 0
        while attempts_stars < 3:
            stars_input = input("Enter the minimum number of stars (press Enter to skip): ").strip()
            if stars_input:
                try:
                    stars = int(stars_input)
                    matching_hotels = self.search_manager.filter_hotels_by_minimum_stars(stars)
                    if not matching_hotels:
                        print("No hotels were found that fulfill the minimum star requirement.")
                    else:
                        for hotel in matching_hotels:
                            print(f"Hotel: {hotel.name}, Stars: {hotel.stars}, Location: {hotel.address.city}")
                        return  # Exit after displaying matching hotels
                except ValueError:
                    print("Invalid input. Please enter a whole number for stars.")
                    attempts_stars += 1
            else:
                break
        if attempts_stars == 3:
            print("Maximum attempts exceeded. Please restart and try again.")


if __name__ == "__main__":
    database_path = "../data/database.db"
    manager = SearchManager(database_path)
    interface = UserInterface(manager)
    #interface.ask_for_location()
    #interface.check_for_booking_date()
    #interface.ask_for_number_of_guests()
    #interface.ask_for_maximum_price()
    #interface.ask_for_minimum_stars()








