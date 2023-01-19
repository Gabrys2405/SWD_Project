from __future__ import annotations
from typing import List, Literal
from PySide6 import QtCore
import numpy as np
import pandas as pd


class EdiTableModel(QtCore.QAbstractTableModel):
    def __init__(self):
        super().__init__()
        self._editable: bool = True

    def flags(self, index):
        if self._editable:
            return QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsEditable
        return 0
    


class DataFrameTableModel(EdiTableModel):
    # Class source: https://www.pythonguis.com/faq/editing-pyqt-tableview/

    def __init__(self, data: pd.DataFrame, editable):
        super().__init__()
        self._data = data

    def rowCount(self, index):
        return self._data.shape[0]

    def columnCount(self, index):
        return self._data.shape[1]

    def data(self, index, role=QtCore.Qt.DisplayRole):
        if index.isValid():
            if role == QtCore.Qt.DisplayRole or role == QtCore.Qt.EditRole:
                value = self._data.values[index.row(), index.column()]
                return str(value)

    def setData(self, index, value, role):
        if role == QtCore.Qt.EditRole:
            try:
                value = float(value)
            except:
                return False
            
            self._data.values[index.row(), index.column()] = value
            print(self._data.values[index.row(), index.column()])
            return True
        return False
    
    def insertRow(self, row: int) -> bool:
        self._data.loc[self._data.shape[0]] = [0] * self._data.shape[1]
        self.layoutChanged.emit()
        return True
    
    def removeRow(self, row: int) -> bool:
        if row > len(self._data)-1 or len(self._data) == 1:
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



class NumPyTableModel(EdiTableModel):
    # Class source: https://www.pythonguis.com/faq/editing-pyqt-tableview/

    def __init__(self, data: np.ndarray, column_data: List[str]):
        super().__init__()
        self._data = data
        self._column_data = column_data

    def rowCount(self, index):
        return self._data.shape[0]

    def columnCount(self, index):
        return self._data.shape[1]

    def data(self, index, role=QtCore.Qt.DisplayRole):
        if index.isValid():
            if role == QtCore.Qt.DisplayRole or role == QtCore.Qt.EditRole:
                value = self._data[index.row(), index.column()]
                return str(value)

    def setData(self, index, value, role):
        if role == QtCore.Qt.EditRole:
            try:
                value = float(value)
            except:
                return False
            
            self._data[index.row(), index.column()] = value
            print(self._data[index.row(), index.column()])
            return True
        return False
    
    def insertRow(self, row: int) -> bool:
        self._data = np.vstack((self._data, [0] * self._data.shape[1]), axis=0)
        self.layoutChanged.emit()
        return True
    
    def removeRow(self, row: int) -> bool:
        if row > len(self._data)-1 or len(self._data) == 1:
            return False
        self._data = np.delete(self._data, row, axis=0)
        self.layoutChanged.emit()
        return True
    
    def setNewData(self, data: np.ndarray):
        self._data = data
        self.layoutChanged.emit()
    
    def headerData(self, col, orientation, role):
        if orientation == QtCore.Qt.Horizontal and role == QtCore.Qt.DisplayRole:
            return self._column_data[col]

    @property
    def data(self):
        return self._data