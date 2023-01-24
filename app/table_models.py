from __future__ import annotations
from typing import List, Callable, Any
from PySide6 import QtCore
import numpy as np
import pandas as pd


class EdiTableModel(QtCore.QAbstractTableModel):
    def __init__(self, editable: bool = True):
        super().__init__()
        self._editable: bool = editable

    def flags(self, index):
        # if self._editable:
            return QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsEditable
        # return QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled
    


class DataFrameTableModel(EdiTableModel):
    # Class source: https://www.pythonguis.com/faq/editing-pyqt-tableview/

    def __init__(self, data: pd.DataFrame, value_converter: Callable[[str], Any] = float, editable: bool = True):
        super().__init__(editable)
        self._data = data
        self._value_converter = value_converter

    def rowCount(self, index):
        return self._data.shape[0]

    def columnCount(self, index):
        return self._data.shape[1]

    def data(self, index, role=QtCore.Qt.DisplayRole):
        if index.isValid():
            if role == QtCore.Qt.DisplayRole or role == QtCore.Qt.EditRole:
                value = self._data.values[index.row(), index.column()]
                if isinstance(value, float):
                    if value >= 100:
                        return str(value)
                    return '{:#.3g}'.format(value)
                return str(value)

    def setData(self, index, value, role):
        if role == QtCore.Qt.EditRole and self._editable:
            try:
                new_value = self._value_converter(value)
            except:
                return False
            self._data.iloc[index.row(), index.column()] = new_value
            # actual_value = self._data.values[index.row(), index.column()]
            # print(f"{value = }, {new_value = }, {actual_value = }, {type(actual_value)}")
            return True
        return False
    
    def insertRow(self, row: int) -> bool:
        if not self._editable:
            return False
        self._data.loc[self._data.shape[0]] = [0] * self._data.shape[1]
        self.layoutChanged.emit()
        return True
    
    def removeRow(self, row: int) -> bool:
        if not self._editable or row > len(self._data)-1 or len(self._data) == 1:
            return False
        self._data.drop(self._data.index[row], inplace=True)
        self.layoutChanged.emit()
        return True
    
    def setNewData(self, data: pd.DataFrame):
        self._data = data
        self.layoutChanged.emit()
    
    def headerData(self, col, orientation, role):
        if orientation == QtCore.Qt.Horizontal and role == QtCore.Qt.DisplayRole:
            return self._data.columns[col]
