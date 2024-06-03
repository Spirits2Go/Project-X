import os
from sqlalchemy import create_engine, select, func, and_, or_, not_
from sqlalchemy.orm import scoped_session, sessionmaker, joinedload
from pathlib import Path
from datetime import datetime
from data_access.data_base import init_db
from data_models.models import *

class SearchUI:
    def __init__(self, database_file):
        database_path = Path(database_file)
        if not database_path.is_file():
            init_db(database_file, generate_example_data=True)
        self.__engine = create_engine(f'sqlite:///{database_file}', echo=False)
        self.__session = scoped_session(sessionmaker(bind=self.__engine))

    def show_search_menu(self):
        while True:
            self.clear()
            print("Search Menu")
            print("1. Search Hotels by Name")
            print("2. Search Hotels by Location")
            print("3. Search Available Rooms by Date")
            print("4. Search Available Rooms by the Number of Guests")
            print("5. Search Hotels by Rating of Stars")
            print("6. Search Hotels by Price")
            print("7. Back to Main Menu")

            choice = input("Enter Option (1-7): ")
            if choice == "1":
                self.search_hotels_by_name()
            elif choice == "2":
                self.ask_for_location()
            elif choice == "3":
                self.check_for_booking_date()
            elif choice == "4":
                self.ask_for_number_of_guests()
            elif choice == "5":
                self.ask_for_minimum_stars()
            elif choice == "6":
                self.ask_for_maximum_price()
            elif choice == "7":
                break
            else:
                print("Invalid choice, please select a valid option.")
                input("Press Enter to continue...")

    def search_hotels_by_name(self):
        name = input("Enter hotel name to search: ")
        hotels = self.get_hotels_by_name(name)
        if hotels:
            for hotel in hotels:
                print(f"Hotel: {hotel.name}, Stars: {hotel.stars}, Address: {hotel.address.city}")
        else:
            print("No hotels found with that name.")
        input("Press Enter to return to search menu...")

    def ask_for_location(self):
        location = input("Enter preferred location (press Enter to skip): ").strip()
        matching_hotels = self.filter_hotels_by_location(location)
        if not matching_hotels:
            print("There aren't any hotels in your preferred location.")
            return
        for hotel in matching_hotels:
            print(f"Hotel: {hotel.name}, Location: {hotel.address.city}")

    def check_for_booking_date(self):
        try:
            city = input("Enter the city to search for available rooms: ").strip()
            check_in_date_str = input("Enter your check-in date (YYYY-MM-DD): ")
            check_out_date_str = input("Enter your check-out date (YYYY-MM-DD): ")
            guests = int(input("Enter number of guests: "))
            stars = input("Enter minimum stars (press Enter to skip): ")
            stars = int(stars) if stars else None

            check_in_date = datetime.strptime(check_in_date_str, '%Y-%m-%d').date()
            check_out_date = datetime.strptime(check_out_date_str, '%Y-%m-%d').date()

            if check_out_date <= check_in_date:
                print("Check-out date must be after check-in date.")
                return

            duration = (check_out_date - check_in_date).days
            available_rooms = self.get_available_rooms(city, check_in_date, check_out_date, guests, stars)

            if not available_rooms:
                print("No rooms available for the selected dates.")
            else:
                print("Available rooms:")
                for room in available_rooms:
                    total_price = self.calculate_total_price(room.price, duration)
                    print(f"Room Number: {room.number}, Type: {room.type}, Price per Night: {room.price} CHF, Total Cost for {duration} Nights: {total_price} CHF in Hotel: {room.hotel.name}, Location: {room.hotel.address.city}")
        except ValueError as e:
            print(f"Error parsing dates, please use the format YYYY-MM-DD: {e}")

    def ask_for_number_of_guests(self):
        matching_hotels = self.get_hotels_by_name('')  # Assuming this returns all hotels when an empty string is passed
        guests = input("Enter the number of guests (press Enter to skip): ").strip()
        if guests:
            try:
                guests = int(guests)
                matching_hotels = self.filter_hotels_by_guests(matching_hotels, guests)
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
                    if room.max_guests >= guests:
                        print(f"Room Number: {room.number}, Capacity: {room.max_guests}")

    def ask_for_maximum_price(self):
        try:
            max_price_input = input("Enter maximum price per room per night (press Enter to skip): ").strip()
            if max_price_input:
                max_price = float(max_price_input)
                rooms_under_price = self.filter_hotels_by_max_price(max_price)
                if not rooms_under_price:
                    print("No rooms found under the price limit provided.")
                else:
                    for room in rooms_under_price:
                        print(f"Room Number: {room.number}, Type: {room.type}, Price: {room.price} in Hotel: {room.hotel.name}, Location: {room.hotel.address.city}")
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
                    matching_hotels = self.filter_hotels_by_minimum_stars(stars)
                    if not matching_hotels:
                        print("No hotels were found that fulfill the minimum star requirement.")
                    else:
                        for hotel in matching_hotels:
                            print(f"Hotel: {hotel.name}, Stars: {hotel.stars}, Location: {hotel.address.city}")
                        return
                except ValueError:
                    print("Invalid input. Please enter a whole number for stars.")
                    attempts_stars += 1
            else:
                break
        if attempts_stars == 3:
            print("Maximum attempts exceeded. Please restart and try again.")

    def get_hotels_by_name(self, name):
        query = select(Hotel).where(Hotel.name.like(f"%{name}%"))
        return self.__session.execute(query).scalars().all()

    def filter_hotels_by_location(self, location):
        if not location:
            return self.__session.execute(select(Hotel)).scalars().all()
        query = select(Hotel).join(Hotel.address).where(func.lower(Address.city) == location.lower())
        return self.__session.execute(query).scalars().all()

    def get_available_rooms(self, city, check_in_date, check_out_date, guests, stars):
        query = (
            select(Room)
            .join(Room.hotel)
            .join(Hotel.address)
            .outerjoin(Booking, and_(
                Room.hotel_id == Booking.room_hotel_id,
                Room.number == Booking.room_number
            ))
            .filter(
                and_(
                    func.lower(Address.city) == city.lower(),
                    Room.max_guests >= guests,
                    or_(
                        Booking.id == None,
                        not_(
                            and_(
                                Booking.start_date < check_out_date,
                                Booking.end_date > check_in_date
                            )
                        )
                    )
                )
            )
            .options(joinedload(Room.bookings), joinedload(Room.hotel).joinedload(Hotel.address))
        )

        if stars:
            query = query.filter(Hotel.stars >= stars)

        result = self.__session.execute(query).unique()
        available_rooms = result.scalars().all()
        return available_rooms

    def calculate_total_price(self, price_per_night, duration):
        total_price = price_per_night * duration
        return round(total_price * 20) / 20  # Rounding to the nearest 0.05 CHF

    def filter_hotels_by_guests(self, hotels, guests):
        filtered_hotels = []
        for hotel in hotels:
            matching_rooms = [room for room in hotel.rooms if room.max_guests >= guests]
            if matching_rooms:
                filtered_hotels.append(hotel)
        return filtered_hotels

    def filter_hotels_by_max_price(self, max_price):
        query = select(Room).join(Hotel).where(Room.price <= max_price).options(joinedload(Room.hotel))
        rooms = self.__session.execute(query).scalars().all()
        return rooms

    def filter_hotels_by_minimum_stars(self, min_stars):
        query = select(Hotel).where(Hotel.stars >= min_stars)
        return self.__session.execute(query).scalars().all()

    @staticmethod
    def clear():
        os.system('cls' if os.name == 'nt' else 'clear')











