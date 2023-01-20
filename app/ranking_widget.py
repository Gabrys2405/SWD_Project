# Type Checking
from __future__ import annotations 
from typing import Optional

# Real imports
from PySide6 import QtCore, QtWidgets
import pandas as pd
from table_models import DataFrameTableModel
from table_widget import EdiTableWidget

from hotel_loader import HotelLoader
from system_wyboru_hoteli import SystemWyboruHoteli
from addons import get_default_font


class RankingWidget(QtWidgets.QWidget):
    def __init__(self, system: SystemWyboruHoteli):
        super().__init__()
        self.system = system

        self._main_layout = QtWidgets.QHBoxLayout(self)
        self.setLayout(self._main_layout)

        self._layout_column_1 = QtWidgets.QVBoxLayout(self)
        self._main_layout.addLayout(self._layout_column_1)
        self._layout_column_2 = QtWidgets.QVBoxLayout(self)
        self._main_layout.addLayout(self._layout_column_2)


        element = QtWidgets.QLabel("W przygotowaniu")
        element.setFont(get_default_font())
        self._layout_column_1.addWidget(element)
