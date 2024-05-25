import os
from business.UserManager import UserManager

def main():
    db_file = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'data', 'database.db'))
    print(f"Database file path: {db_file}")

    if not os.path.exists(db_file):
        print(f"Database file does not exist: {db_file}")
        return

    user_manager = UserManager(db_file)
    user = None

    while True:
        print("\nWelcome to the Hotel Booking System")
        print("1. Login")
        print("2. View Booking History")
        print("3. Create Booking")
        print("4. Update Booking")
        print("5. Delete Booking")
        print("6. Exit")
        choice = input("Please select an option: ").strip()

        if choice.isdigit():
            choice = int(choice)
        else:
            print("Invalid choice. Please enter a number.")
            continue

        if choice == 1:
            username = input("Enter username: ").strip()
            password = input("Enter password: ").strip()
            user = user_manager.login(username, password)
            if user:
                print("Login successful")
            else:
                print("Invalid username or password")
        elif choice == 2:
            if user:
                bookings = user_manager.get_booking_history(user.id)
                if bookings:
                    print("Booking History:")
                    for booking in bookings:
                        print(booking)
                else:
                    print("No booking history found.")
            else:
                print("Please login first.")
        elif choice == 3:
            if user:
                room_id = int(input("Enter room ID: ").strip())
                start_date = input("Enter start date (YYYY-MM-DD): ").strip()
                end_date = input("Enter end date (YYYY-MM-DD): ").strip()
                number_of_guests = int(input("Enter number of guests: ").strip())
                comment = input("Enter comment: ").strip()
                user_manager.create_booking(user.id, room_id, start_date, end_date, number_of_guests, comment)
                print("Booking created successfully.")
            else:
                print("Please login first.")
        elif choice == 4:
            if user:
                booking_id = int(input("Enter booking ID to update: ").strip())
                room_id = int(input("Enter new room ID: ").strip())
                start_date = input("Enter new start date (YYYY-MM-DD): ").strip()
                end_date = input("Enter new end date (YYYY-MM-DD): ").strip()
                number_of_guests = int(input("Enter new number of guests: ").strip())
                comment = input("Enter new comment: ").strip()
                user_manager.update_booking(booking_id, room_id, start_date, end_date, number_of_guests, comment)
                print("Booking updated successfully.")
            else:
                print("Please login first.")
        elif choice == 5:
            if user:
                booking_id = int(input("Enter booking ID to delete: ").strip())
                user_manager.delete_booking(booking_id)
                print("Booking deleted successfully.")
            else:
                print("Please login first.")
        elif choice == 6:
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
