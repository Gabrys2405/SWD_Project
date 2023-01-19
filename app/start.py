from PySide6 import QtCore, QtWidgets
from hotel_loader import HotelLoader
from system_wyboru_hoteli import SystemWyboruHoteli
from main_screen import MainScreen

def start():
    """Uruchomienie GUI aplikacji"""

    print("Start")

    app = QtWidgets.QApplication([])

    # Zapewnienie, że jako znak dziesiętny będzie kropka
    QtCore.QLocale.setDefault(QtCore.QLocale.C)

    system = SystemWyboruHoteli()

    widget = MainScreen(system)
    widget.resize(1360, 720)
    # widget.setMinimumWidth(500)
    widget.show()

    app.exec()


if __name__ == "__main__":
    start()