from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QLineEdit, QPushButton, QTableView, QHeaderView
from PyQt5.QtCore import Qt, QAbstractTableModel, QModelIndex

from sqlalchemy import func
from sqlalchemy.orm import Session

from data_models.models import *


class HotelTableView(QMainWindow):
    def __init__(self, session, *args):
        QMainWindow.__init__(self, *args)
        uic.loadUi("./gui/hotel_search.ui", self)
        self.txt_name: QLineEdit = self.txt_name
        self.btn_search: QPushButton = self.btn_search
        self.hotelTableView: QTableView = self.hotelTableView
        self.session = session
        self.hotelTableModel = HotelTableModel(self, self.session)
        self.hotelTableModel.all()
        self.hotelTableView.setModel(self.hotelTableModel)

        self.hotelTableView.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeToContents)
        self.hotelTableView.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeToContents)
        self.hotelTableView.horizontalHeader().setSectionResizeMode(2, QHeaderView.ResizeToContents)
        self.hotelTableView.horizontalHeader().setSectionResizeMode(3, QHeaderView.Stretch)

        self.btn_search.clicked.connect(self.btn_search_clicked)

    def btn_search_clicked(self):
        self.hotelTableModel.search_name(self.txt_name.text())
        self.hotelTableView.viewport().update()


class HotelTableModel(QAbstractTableModel):
    id = "Id"
    name = "Name"
    number_of_rooms = "# of rooms"
    address = "Address"

    def __init__(self, parent, session: Session, *args) -> None:
        QAbstractTableModel.__init__(self, parent, *args)
        self.header = [
            HotelTableModel.id,
            HotelTableModel.name,
            HotelTableModel.number_of_rooms,
            HotelTableModel.address
        ]
        self.session = session
        self.hotels: List[Hotel] = []

    def all(self):
        self.hotels = self.session.query(Hotel).all()

    def search_name(self, like: str):
        like = like.lower()
        self.hotels = self.session.query(Hotel).filter(func.lower(Hotel.name).like(f'%{like}%')).all()

    def rowCount(self, parent: QModelIndex = ...) -> int:
        return len(self.hotels)

    def columnCount(self, parent: QModelIndex = ...) -> int:
        return len(self.header)

    def data(self, index: QModelIndex, role: int = ...):
        if not index.isValid():
            return None
        if role == Qt.DisplayRole:
            if self.header[index.column()] == HotelTableModel.id:
                return self.hotels[index.row()].id
            elif self.header[index.column()] == HotelTableModel.name:
                return self.hotels[index.row()].name
            elif self.header[index.column()] == HotelTableModel.number_of_rooms:
                return len(self.hotels[index.row()].rooms)
            elif self.header[index.column()] == HotelTableModel.address:
                return f"{self.hotels[index.row()].address.street}, {self.hotels[index.row()].address.zip} {self.hotels[index.row()].address.city}"

    def headerData(self, section: int, orientation: Qt.Orientation, role: int = ...):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return self.header[section]
