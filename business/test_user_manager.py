import os
from datetime import date
from business.UserManager import UserManager

# Get the absolute path to the database file relative to the project root
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
db_path = os.path.join(project_root, 'data', 'database.db')
print("Current working directory:", os.getcwd())
print("Database file path:", db_path)

user_manager = UserManager(db_path)

# Test login functionality
user = user_manager.login("laura.jackson@bluemail.ch", "SuperSecret")
if user:
    user_id = user.id

    # Test get booking history
    print("\nBooking History:")
    user_manager.get_booking_history(user_id)

    # Test create a new booking
    print("\nCreating a new booking:")
    user_manager.create_booking(user_id, 1, '01', date(2024, 6, 1), date(2024, 6, 5), 2, "Vacation")

    # Test update booking
    print("\nUpdating booking:")
    user_manager.update_booking(1, comment="Updated Comment")

    # Test delete booking
    print("\nDeleting booking:")
    user_manager.delete_booking(1)
