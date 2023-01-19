# Type Checking
from __future__ import annotations  # naprawa cyrkulacji importów
from typing import Optional, List

# Real imports
from PySide6 import QtCore, QtWidgets
import pandas as pd
from table_models import DataFrameTableModel
from table_widget import EdiTableWidget

from hotel_loader import HotelLoader
from system_wyboru_hoteli import SystemWyboruHoteli



class MainScreen(QtWidgets.QWidget):

    def __init__(self, system: SystemWyboruHoteli):
        super().__init__()
        self.system = system
        self.plik_bazy: str = "(brak)"

        self._tabele_zrodlowe_utworzone: bool = False

        self.setWindowTitle("System Wyboru Hoteli - Zakopane")

        self._main_layout = QtWidgets.QHBoxLayout(self)
        self.setLayout(self._main_layout)

        self._layout_column_1 = QtWidgets.QVBoxLayout(self)
        self._main_layout.addLayout(self._layout_column_1)
        self._layout_column_2 = QtWidgets.QVBoxLayout(self)
        self._main_layout.addLayout(self._layout_column_2)

        
        element = QtWidgets.QPushButton("Wczytaj plik bazy...")
        element.clicked.connect(self.wczytaj_baze)
        self._layout_column_1.addWidget(element)


    def utworz_tabele_zrodlowe(self):
        if self._tabele_zrodlowe_utworzone:
            return
        self._tabele_zrodlowe_utworzone = True

        system = self.system
        system.utworz_dataframey()
        self._utworz_jedna_tabele(
            self._layout_column_1,
            "Minimalne wartości kryteriów",
            system.minimalne_kryteria,
            True, False
        )
        self._utworz_jedna_tabele(
            self._layout_column_1,
            "Maksymalne wartości kryteriów",
            system.maksymalne_kryteria,
            True, False
        )
        self._utworz_jedna_tabele(
            self._layout_column_1,
            "Punkty docelowe",
            system.punkty_docelowe,
            True, True
        )
        self._utworz_jedna_tabele(
            self._layout_column_1,
            "Punkty status-quo",
            system.punkty_status_quo,
            True, True
        )


    def _utworz_jedna_tabele(
            self, 
            layout: QtWidgets.QLayout,
            tytul: str,
            dataframe: pd.DataFrame,
            edytowalna: bool = True, 
            przyciski_edycji: bool = True
        ):
        element = QtWidgets.QLabel(tytul, alignment=QtCore.Qt.AlignHCenter)
        font = element.font()
        font.setBold(True)
        font.setPixelSize(16)
        element.setFont(font)
        layout.addWidget(element)

        table_widget = EdiTableWidget()
        model = DataFrameTableModel(dataframe, edytowalna)
        table_widget.setModel(model)
        h = table_widget.horizontalHeader()
        for i, _ in enumerate(dataframe.columns):
            h.setSectionResizeMode(i, QtWidgets.QHeaderView.ResizeMode.Stretch)

        if przyciski_edycji:
            table_widget.addRowManagementButtons()
        else:
            table_widget.setFixedHeight(70)
        layout.addWidget(table_widget)


    def wczytaj_baze(self):
        fname = QtWidgets.QFileDialog.getOpenFileName(
            self, 'Wczytaj bazę z pliku...', None, 
            "Plik programu Excel (*.xlsx);;Plik CSV (*.csv)"
        )
        if fname[0]:
            try:
                baza = HotelLoader().zaladuj_plik(fname[0]).jako_dataframe()
            except Exception as e:
                self.wyswietl_blad("Błąd wczytywania bazy danych", e)
                return
            self.system.dane_hoteli = baza
            self.plik_bazy = fname[0]
            self.utworz_tabele_zrodlowe()
            print(self.plik_bazy)
    

    def wyswietl_blad(self, label: str, exception: Exception):
        dialog = QtWidgets.QMessageBox()
        dialog.setWindowTitle(label)
        dialog.setText(f"{label}\n\n{str(exception)}")
        dialog.exec()