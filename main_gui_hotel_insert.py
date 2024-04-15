import sys

from PyQt5.QtWidgets import QApplication

from gui.hotel_insert import HotelUIForm

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = HotelUIForm()
    window.show()
    sys.exit(app.exec())
