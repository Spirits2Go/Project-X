import os
from business.HotelManagement import HotelManager
from business.ReservationManager import ReservationManager
from business.UserManager import UserManager
from ui.SearchUI import SearchUI
from ui.ReservationUI import ReservationUI
from ui.AdminUI import AdminUI

class Console(object):
    def __init__(self):
        pass

    def run(self):
        raise NotImplementedError("Implement this method")

    @staticmethod
    def clear():
        os.system('cls' if os.name == 'nt' else 'clear')


class Application(object):
    def __init__(self, start: Console):
        self._current: Console = start

    def run(self):
        while self._current:
            self._current = self._current.run()


class MenuOption(object):
    def __init__(self, title):
        self._title = title

    def get_title(self) -> str:
        return self._title

    def __str__(self):
        return self._title

    def __len__(self):
        return len(self._title)


class Menu(Console):
    def __init__(self, title, width=50):
        super().__init__()
        self._title = title
        self._options = []
        self._width = width

    def __iter__(self):
        return iter(self._options)

    def get_options(self) -> list:
        return self._options

    def add_option(self, option: MenuOption):
        self._options.append(option)

    def remove_option(self, option: MenuOption):
        self._options.remove(option)

    def _show(self):
        print("#" * self._width)
        left = "# "
        right = "#"
        space = " " * (self._width - len(left) - len(self._title) - len(right))
        print(f"{left}{self._title}{space}{right}")
        print("#" * self._width)
        for i, option in enumerate(self._options, 1):
            index = f"{i}: "
            space = " " * (self._width - len(left) - len(index) - len(option) - len(right))
            print(f"{left}{index}{option}{space}{right}")
        print("#" * self._width)

    def _make_choice(self) -> int:
        choice = input("Enter Option: ")
        options = [f"{i}" for i, option in enumerate(self._options, 1)]
        while choice not in options:
            self._show()
            print("Invalid Option")
            choice = input("Enter Option: ")
        return int(choice)

    def _navigate(self, choice: int):
        raise NotImplementedError("Implement this method")

    def run(self) -> Console:
        self.clear()
        self._show()
        return self._navigate(self._make_choice())


class MainMenu(Menu):
    def __init__(self, db_file):
        super().__init__("Main Menu")
        self.hotel_manager = HotelManager(db_file)
        self.reservation_manager = ReservationManager(db_file)
        self.user_manager = UserManager(db_file)
        self.search_ui = SearchUI(self.hotel_manager)
        self.reservation_ui = ReservationUI(self.reservation_manager, self.user_manager)
        self.admin_ui = AdminUI(self.hotel_manager, self.reservation_manager)
        self.add_option(MenuOption("Search Hotels"))
        self.add_option(MenuOption("Book a Room"))
        self.add_option(MenuOption("User Management"))
        self.add_option(MenuOption("Admin Management"))
        self.add_option(MenuOption("Quit"))

    def show_menu(self):
        self._show()

    def user_choice(self):
        return self._make_choice()

    def _navigate(self, choice: int) -> Console:
        match choice:
            case 1:
                self.search_ui.show_search_menu()
                return self
            case 2:
                self.reservation_ui.show_reservation_menu()
                return self
            case 3:
                self.user_manager.show_user_menu()
                return self
            case 4:
                self.admin_ui.show_admin_menu()
                return self
            case 5:
                return None
            case _:
                print("Invalid choice, please select a valid option.")
                return self
