import sys
from pathlib import Path
import os

# Add the project root to sys.path
project_root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(project_root))

from ui.SearchUI import SearchUI
from ui.ReservationUI import ReservationUI
from ui.AdminUI import AdminUI
from business.UserManager import UserManager

class MainMenu:
    def __init__(self, db_file):
        self.user_manager = UserManager(db_file)
        self.search_ui = SearchUI(db_file)
        self.reservation_ui = ReservationUI(db_file, self.user_manager)
        self.admin_ui = AdminUI(db_file, self.user_manager)
        self.logged_in_user = None

    def show_menu(self):
        while True:
            self.clear()
            print("Main Menu")
            print("1. Search Hotels")
            print("2. Book a Room")
            print("3. Admin Management")
            print("4. Create User")
            print("5. Log Out" if self.user_manager.is_logged_in() else "5. Log In")
            print("6. Quit")

            choice = input("Enter Option (1-6): ")
            if choice == "1":
                self.search_ui.show_search_menu()
            elif choice == "2":
                self.reservation_ui.show_reservation_menu()
            elif choice == "3":
                if self.user_manager.is_logged_in():
                    role = self.user_manager.get_user_role(self.user_manager.get_current_user())
                    if role == 'administrator':
                        self.admin_ui.show_admin_menu()
                    else:
                        print("Access denied. You must be an admin to access this menu.")
                        input("Press Enter to continue...")
                else:
                    print("You must log in to access the admin menu.")
                    input("Press Enter to continue...")
            elif choice == "4":
                self.create_user()
            elif choice == "5":
                if self.user_manager.is_logged_in():
                    self.logout()
                else:
                    self.login()
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
            self.logged_in_user = user
            input("Press Enter to continue...")
        else:
            print("Login failed")
            input("Press Enter to continue...")

    def logout(self):
        self.user_manager.logout()
        self.logged_in_user = None
        print("Logged out successfully")
        input("Press Enter to continue...")

    def create_user(self):
        role_mapping = {
            "user": "registered_user",
            "admin": "administrator"
        }
        print("Available roles: user, admin")
        role_input = input("Enter your role: ").strip().lower() or 'user'
        role = role_mapping.get(role_input, 'registered_user')
        username = input("Enter new username: ")
        password = input("Enter new password: ")
        new_user = self.user_manager.create_user(username, password, role)
        if new_user:
            print(f"User created: {new_user.username}")
        else:
            print("Failed to create user. Please ensure the role exists.")
        input("Press Enter to continue...")

    @staticmethod
    def clear():
        os.system('cls' if os.name == 'nt' else 'clear')


if __name__ == "__main__":
    current_ui = MainMenu("../data/database.db")
    current_ui.show_menu()
