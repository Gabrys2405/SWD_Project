# Type Checking
from __future__ import annotations  # naprawa cyrkulacji importów

# Real imports
from PySide6 import QtWidgets
from system_wyboru_hoteli import SystemWyboruHoteli
from params_widget import ParamsWidget
from ranking_widget import RankingWidget
from porownanie_widget import PorownanieWidget


class MainWidget(QtWidgets.QWidget):
    def __init__(self, system: SystemWyboruHoteli) -> None:
        super().__init__()
        self.setWindowTitle("System Wyboru Hoteli - Zakopane")

        layout = QtWidgets.QVBoxLayout()
        self.setLayout(layout)

        self.tabWidget = QtWidgets.QTabWidget()
        layout.addWidget(self.tabWidget)

        self.tabWidget.addTab(
            ParamsWidget(system),
            "Parametry"
        )
        self.tabWidget.addTab(
            RankingWidget(system),
            "Rankingi"
        )
        self.tabWidget.addTab(
            PorownanieWidget(),
            "Rankingi"
        )

