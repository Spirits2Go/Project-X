import sys

from PyQt5 import QtCore, QtGui
from PyQt5 import uic
from PyQt5.QtWidgets import QLineEdit, QComboBox, QPushButton, QMainWindow, QApplication, QMessageBox
from sqlalchemy import create_engine, exc
from sqlalchemy.orm import Session

from data_models.models import *


class NameAddressValidator(QtGui.QRegularExpressionValidator):
    validationChanged = QtCore.pyqtSignal(QtGui.QValidator.State)

    def validate(self, _input, pos):
        state, _input, pos = super().validate(_input, pos)
        self.validationChanged.emit(state)
        return state, _input, pos


class HotelUIForm(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("./gui/hotel_creation.ui", self)

        # GUI controls
        self.lineEdit_name: QLineEdit = self.lineEdit_name
        self.comboBox_sterne: QComboBox = self.comboBox_sterne
        self.lineEdit_strasse: QLineEdit = self.lineEdit_strasse
        self.lineEdit_plz: QLineEdit = self.lineEdit_plz
        self.lineEdit_ort: QLineEdit = self.lineEdit_ort
        self.comboBox_anzahl_zimmer: QComboBox = self.comboBox_anzahl_zimmer
        self.pushButton_speichern: QPushButton = self.pushButton_speichern
        self.pushButton_abbrechen: QPushButton = self.pushButton_abbrechen
        self.pushButton_clear: QPushButton = self.pushButton_clear

        # Aktion für Button "Speichern"
        self.pushButton_speichern.clicked.connect(self.save_to_db)

        # Aktion für Button "Abbrechen"
        self.pushButton_abbrechen.clicked.connect(self.quit_app)

        # Aktion für Button "Clear"
        self.pushButton_clear.clicked.connect(self.clear_input)

        # Customizing QComboBox "Sterne"
        self.comboBox_sterne.addItems(["1", "2", "3", "4", "5"])

        # Customizing QComboBox "Anzahl Zimmer"
        self.comboBox_anzahl_zimmer.addItems(["1", "2", "3", "4", "5", "6", "7", "8", "9", "10"])

        # Validators für Hotelname / Adresse (mit QValidator)
        # Validierung für Hotelname
        global name_validator
        name_regexp = QtCore.QRegularExpression(r'^[a-zA-Z0-9 ]{4,}$')
        name_validator = NameAddressValidator(name_regexp, self)
        name_validator.validationChanged.connect(self.handle_validation_change_name)
        self.lineEdit_name.setValidator(name_validator)

        # Validierung für Strasse
        global strasse_validator
        strasse_regexp = QtCore.QRegularExpression(r'^[a-zA-Z0-9 \\.\\-]{5,}$')
        strasse_validator = NameAddressValidator(strasse_regexp, self)
        strasse_validator.validationChanged.connect(self.handle_validation_change_strasse)
        self.lineEdit_strasse.setValidator(strasse_validator)

        # Validierung für PLZ
        global plz_validator
        plz_regexp = QtCore.QRegularExpression(r'^[0-9]{4}$')
        plz_validator = NameAddressValidator(plz_regexp, self)
        plz_validator.validationChanged.connect(self.handle_validation_change_plz)
        self.lineEdit_plz.setValidator(plz_validator)

        # Validierung für Ort
        global ort_validator
        ort_regexp = QtCore.QRegularExpression(r'^[a-zA-Z]{4,}$')
        ort_validator = NameAddressValidator(ort_regexp, self)
        ort_validator.validationChanged.connect(self.handle_validation_change_ort)
        self.lineEdit_ort.setValidator(ort_validator)

    # Speichern der Hotels in DB
    def save_to_db(self):
        result_name, _, _ = name_validator.validate(self.lineEdit_name.text(), 0)
        result_strasse, _, _ = strasse_validator.validate(self.lineEdit_strasse.text(), 0)
        result_plz, _, _ = plz_validator.validate(self.lineEdit_plz.text(), 0)
        result_ort, _, _ = ort_validator.validate(self.lineEdit_ort.text(), 0)

        if result_name and result_strasse and result_plz and result_ort == QtGui.QValidator.Acceptable == QtGui.QValidator.Acceptable:
            engine = create_engine("sqlite:///data/example.db", echo=True)
            try:
                engine.connect()
                print("Connection successful")
            except SQLAlchemyError as err:
                print("Connection not successful", err.__cause__)

            hotel_name = self.lineEdit_name.text()
            hotel_sterne = int(self.comboBox_sterne.currentText())
            adresse_strasse = self.lineEdit_strasse.text()
            adresse_plz = self.lineEdit_plz.text()
            adresse_ort = self.lineEdit_ort.text()

            with Session(engine) as session:
                try:
                    hotel = Hotel(name=hotel_name, stars=hotel_sterne,
                                  address=Address(street=adresse_strasse,
                                                  zip=adresse_plz,
                                                  city=adresse_ort))
                    session.add(hotel)
                    session.commit()

                except exc.SQLAlchemyError:
                    QMessageBox.question(self, "Message",
                                         "Fehler bei Speicherung in Datenbank!",
                                         QMessageBox.Ok)

        else:
            QMessageBox.question(self, "Message", "Validierung des Formulars enthält Fehler!", QMessageBox.Ok)

    # App schliessen
    def quit_app(self):
        reply = QMessageBox.question(self, "Message", "Sind Sie sicher, dass Sie die Anwendung verlassen wollen?",
                                     QMessageBox.Close | QMessageBox.Cancel)

        if reply == QMessageBox.Close:
            app.quit()

    # Lösche Input Daten
    def clear_input(self):
        self.lineEdit_name.clear()
        self.lineEdit_strasse.clear()
        self.lineEdit_plz.clear()
        self.lineEdit_ort.clear()
        # Defaults for Combo Boxes = 1
        self.comboBox_sterne.setCurrentText("1")
        self.comboBox_anzahl_zimmer.setCurrentText("1")

    def handle_validation_change_name(self, state):
        global colour
        if state == QtGui.QValidator.Invalid:
            colour = 'red'
        elif state == QtGui.QValidator.Intermediate:
            colour = 'yellow'
        elif state == QtGui.QValidator.Acceptable:
            colour = 'green'
        self.lineEdit_name.setStyleSheet('border: 3px solid %s' % colour)

    def handle_validation_change_strasse(self, state):
        global colour
        if state == QtGui.QValidator.Invalid:
            colour = 'red'
        elif state == QtGui.QValidator.Intermediate:
            colour = 'yellow'
        elif state == QtGui.QValidator.Acceptable:
            colour = 'green'
        self.lineEdit_strasse.setStyleSheet('border: 3px solid %s' % colour)

    def handle_validation_change_plz(self, state):
        global colour
        if state == QtGui.QValidator.Invalid:
            colour = 'red'
        elif state == QtGui.QValidator.Intermediate:
            colour = 'yellow'
        elif state == QtGui.QValidator.Acceptable:
            colour = 'green'
        self.lineEdit_plz.setStyleSheet('border: 3px solid %s' % colour)

    def handle_validation_change_ort(self, state):
        global colour
        if state == QtGui.QValidator.Invalid:
            colour = 'red'
        elif state == QtGui.QValidator.Intermediate:
            colour = 'yellow'
        elif state == QtGui.QValidator.Acceptable:
            colour = 'green'
        self.lineEdit_ort.setStyleSheet('border: 3px solid %s' % colour)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = HotelUIForm()
    window.show()
    sys.exit(app.exec())
