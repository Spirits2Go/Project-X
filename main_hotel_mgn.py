from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.scoping import scoped_session

from console.console_base import *
from data_access.data_base import *
from data_models.models import *


class HotelManager(object):
    def __init__(self, session_maker):
        self._session = scoped_session(session_maker)

    def show_all_hotels(self):
        hotels = self._session.query(Hotel).all()
        for hotel in hotels:
            print(hotel)
        input("Press Enter to continue...")

    def create_new_hotel(self):
        Console.clear()
        print("Creating new Hotel")
        hotel_name = input("Hotel Name: ")
        hotel_stars = input("Hotel Stars: ")
        hotel_street = input("Hotel Street: ")
        hotel_city = input("Hotel City: ")
        hotel_zip = input("Hotel Zip: ")

        new_address = Address(street=hotel_street, zip=hotel_zip, city=hotel_city)
        new_hotel = Hotel(name=hotel_name, stars=hotel_stars,
                          address=new_address)
        Console.clear()
        print(new_hotel)

        answer = input("Should this hotel be stored? (y/n): ").lower()
        while answer not in ["y", "n"]:
            print("Invalid input. Please try again.")
            answer = input("Should this hotel be stored in another hotel? (Y/n): ").lower()
        match answer:
            case "y":
                self._session.add(new_hotel)
                self._session.commit()
                print("Saved!")
                input("Press Enter to continue...")
            case "n":
                print("Save aborted!")
                input("Press Enter to continue...")


class HotelManagementMenu(Menu):
    def __init__(self, back: Menu):
        super().__init__("Hotel Management")
        self._options.append(MenuOption("Create new Hotel"))
        self._options.append(MenuOption("Show all Hotels"))
        self._options.append(MenuOption("Back"))
        self._back = back

        self._hotel_manager = HotelManager(session_factory)

    def _navigate(self, choice: int):
        match choice:
            case 1:
                self._hotel_manager.create_new_hotel()
                return self
            case 2:
                self._hotel_manager.show_all_hotels()
                return self
            case 3:
                return self._back


class MainMenu(Menu):
    def __init__(self):
        super().__init__("Main Menu")
        self._options.append(MenuOption("Hotel Management"))
        self._options.append(MenuOption("Quit"))
        self.hotel_mgn_menu = HotelManagementMenu(self)

    def _navigate(self, choice: int):
        match choice:
            case 1:
                return self.hotel_mgn_menu
            case 2:
                session = scoped_session(session_factory)
                session.close()
                return None


if __name__ == '__main__':
    DB_FILE = './data/hotel_reservation.db'
    ALWAYS_CREATE_NEW_DB = True
    TEST_DATA = True
    if ALWAYS_CREATE_NEW_DB:
        init_db(DB_FILE, generate_example_data=TEST_DATA)
    else:
        if not os.path.exists(DB_FILE):
            init_db(DB_FILE, generate_example_data=TEST_DATA)
    engine = create_engine(f'sqlite:///{DB_FILE}', echo=False)
    session_factory = sessionmaker(bind=engine)
    app = Application(MainMenu())
    app.run()
