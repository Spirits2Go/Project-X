import os
import sys
from pathlib import Path

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication

from sqlalchemy import create_engine

from sqlalchemy import create_engine, func
from sqlalchemy.schema import CreateTable
from data_access.data_base import *
from data_access.data_generator import *
from gui.hotel_search import *


DB_PATH = './data/hotel_reservation.db'



def main():
    init_db(DB_PATH, True, True, True)
    engine = create_engine(f"sqlite:///{DB_PATH}")

    with Session(engine) as session:
        app = QApplication(sys.argv)
        main_window = HotelTableView(session)
        main_window.show()
        sys.exit(app.exec_())


if __name__ == "__main__":
    main()
