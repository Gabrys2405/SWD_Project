from PySide6 import QtCore, QtWidgets
from system_wyboru_hoteli import SystemWyboruHoteli
from main_widget import MainWidget

def start():
    """Uruchomienie GUI aplikacji"""

    print("Start")

    app = QtWidgets.QApplication([])

    # Zapewnienie, że jako znak dziesiętny będzie kropka
    QtCore.QLocale.setDefault(QtCore.QLocale.C)

    system = SystemWyboruHoteli()

    # FIXME usuń kod debugowania
    # from matplotlib import pyplot as plt
    # def plotter(*args, **kwargs):
    #     plt.figure()
    #     plt.plot([1, 2, 3], [2, 3, 2])
    #     plt.show()
    #     plt.figure()
    #     plt.plot([1, 2, 3], [5, 4, 3])
    #     plt.show()
    #     plt.figure()
    #     plt.plot([1, 2, 3], [10, -1, -1])
    #     plt.show()
    # system.wygeneruj_ranking = plotter

    widget = MainWidget(system)
    widget.resize(1360, 720)
    # widget.setMinimumWidth(500)
    widget.show()

    app.exec()


if __name__ == "__main__":
    start()