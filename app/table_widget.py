# Type Checking
from __future__ import annotations  # naprawa cyrkulacji importów
from typing import Optional

# Real imports
from PySide6 import QtCore, QtWidgets
import numpy as np
import pandas as pd
from addons import get_default_font


class EdiTableWidget(QtWidgets.QWidget):
    def __init__(self, parent: Optional[QtWidgets.QWidget] = None, f: QtCore.Qt.WindowFlags = QtCore.Qt.WindowFlags()) -> None:
        super().__init__(parent, f)

        self._buttons_added: bool = False

        self._layout = QtWidgets.QVBoxLayout()
        self.setLayout(self._layout)

        self._table_widget = QtWidgets.QTableView(self)
        self._table_widget.setFont(get_default_font())
        self._layout.addWidget(self._table_widget)
    

    def addRowManagementButtons(self):
        if not self._buttons_added:
            self._buttons_added = True
            buts = QtWidgets.QHBoxLayout()
            element = QtWidgets.QPushButton("+")
            element.clicked.connect(self.insertRow)
            buts.addWidget(element)
            element = QtWidgets.QPushButton("-")
            element.clicked.connect(self.removeRow)
            buts.addWidget(element)
            self._layout.addLayout(buts)
    

    def insertRow(self):
        model = self.model()
        model.insertRow(model.rowCount(0))


    def removeRow(self):
        index = self._table_widget.currentIndex()
        if index.isValid():
            self.model().removeRow(index.row())


    def model(self) -> QtCore.QAbstractItemModel:
        return self._table_widget.model()
    

    def setModel(self, m: QtCore.QAbstractItemModel):
        self._table_widget.setModel(m)


    def horizontalHeader(self) -> QtWidgets.QHeaderView:
        return self._table_widget.horizontalHeader()
