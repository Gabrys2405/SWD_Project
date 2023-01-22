# Type Checking
from __future__ import annotations  # naprawa cyrkulacji importów
from typing import Optional, Callable, Any

# Real imports
from PySide6 import QtCore, QtWidgets
import pandas as pd
from table_models import DataFrameTableModel
from table_widget import EdiTableWidget

from hotel_loader import HotelLoader
from system_wyboru_hoteli import SystemWyboruHoteli
from addons import get_default_font, converter__str_to_bool


class ParamsWidget(QtWidgets.QWidget):

    def __init__(self, system: SystemWyboruHoteli):
        super().__init__()
        self.system = system
        self.plik_bazy: str = "(brak)"

        self._tabele_zrodlowe_utworzone: bool = False

        self._main_layout = QtWidgets.QHBoxLayout(self)
        self.setLayout(self._main_layout)

        self._layout_column_1 = QtWidgets.QVBoxLayout(self)
        self._main_layout.addLayout(self._layout_column_1)
        self._layout_column_2 = QtWidgets.QVBoxLayout(self)
        self._main_layout.addLayout(self._layout_column_2)


        # LEWA KOLUMNA

        element = QtWidgets.QPushButton("Wczytaj plik bazy...")
        element.clicked.connect(self.wczytaj_baze)
        self._layout_column_1.addWidget(element)


        self.t_hotele = self._utworz_pusta_tabele(
            self._layout_column_1,
            "Hotele",
            przyciski_edycji=False,
            jedno_pole_edytowania=False
        )


        # PRAWA KOLUMNA

        self.t_wybrane_kyteria = self._utworz_pusta_tabele(
            self._layout_column_2,
            "Kryteria uwzględniane w rankingu",
            przyciski_edycji=False,
            jedno_pole_edytowania=True
        )

        row = QtWidgets.QHBoxLayout()

        element = QtWidgets.QLabel("Czy jest wymagany bezpłatny parking?")
        element.setFont(get_default_font())
        row.addWidget(element)

        element = QtWidgets.QCheckBox()
        element.stateChanged.connect(self._przelacz_przymus_parkingu)
        row.addWidget(element)

        self._layout_column_2.addLayout(row)


        self.t_min_kyteria = self._utworz_pusta_tabele(
            self._layout_column_2,
            "Minimalne wartości kryteriów",
            przyciski_edycji=False,
            jedno_pole_edytowania=True
        )
        self.t_max_kyteria = self._utworz_pusta_tabele(
            self._layout_column_2,
            "Maksymalne wartości kryteriów",
            przyciski_edycji=False,
            jedno_pole_edytowania=True
        )

        element = QtWidgets.QLabel("WYPEŁNIA EKSPERT", alignment=QtCore.Qt.AlignHCenter)
        font = get_default_font()
        font.setItalic(True)
        # font.setPixelSize(16)
        element.setFont(font)
        element.setStyleSheet("border-top: 1px double black; padding-top: 5px")
        self._layout_column_2.addWidget(element)

        self.t_p_docelowe = self._utworz_pusta_tabele(
            self._layout_column_2,
            "Punkty docelowe",
            przyciski_edycji=True,
            jedno_pole_edytowania=False
        )
        self.t_p_status_quo = self._utworz_pusta_tabele(
            self._layout_column_2,
            "Punkty status-quo",
            przyciski_edycji=True,
            jedno_pole_edytowania=False
        )

        # FIXME Tymczasowe ładowanie
        self.wczytaj_baze("../Dane/Hotele SWD - importowalne.xlsx")


    def odswiez_dane_tabel(self):
        system = self.system.dane
        self._odswiez_model_w_tabeli(
            self.t_hotele, system.dane_hoteli,
            edytowalna=False
        )
        self._odswiez_model_w_tabeli(
            self.t_wybrane_kyteria, system.wybrane_kryteria, 
            True, converter__str_to_bool
        )
        self._odswiez_model_w_tabeli(
            self.t_min_kyteria, system.minimalne_kryteria, 
            edytowalna=True
        )
        self._odswiez_model_w_tabeli(
            self.t_max_kyteria, system.maksymalne_kryteria, 
            edytowalna=True
        )
        self._odswiez_model_w_tabeli(
            self.t_p_docelowe, system.punkty_docelowe, 
            edytowalna=True
        )
        self._odswiez_model_w_tabeli(
            self.t_p_status_quo, system.punkty_status_quo, 
            edytowalna=True
        )
    

    def _odswiez_model_w_tabeli(
            self, 
            table: EdiTableWidget, 
            dataframe: pd.DataFrame, 
            edytowalna: bool = True,
            value_converter: Callable[[str], Any] = float
        ) -> DataFrameTableModel:
        model = DataFrameTableModel(dataframe, value_converter, editable=edytowalna)
        table.setModel(model)
        h = table.horizontalHeader()
        for i, _ in enumerate(dataframe.columns):
            h.setSectionResizeMode(i, QtWidgets.QHeaderView.ResizeMode.Stretch)


    def _utworz_pusta_tabele(
            self, 
            layout: QtWidgets.QLayout,
            tytul: str,
            przyciski_edycji: bool = True,
            jedno_pole_edytowania: bool = False
        ) -> EdiTableWidget:
        element = QtWidgets.QLabel(tytul, alignment=QtCore.Qt.AlignHCenter)
        font = get_default_font()
        font.setBold(True)
        # font.setPixelSize(16)
        element.setFont(font)
        layout.addWidget(element)

        table_widget = EdiTableWidget()

        if przyciski_edycji:
            table_widget.addRowManagementButtons()
        if jedno_pole_edytowania:
            table_widget.setFixedHeight(70)
        layout.addWidget(table_widget)
        return table_widget


    def _przelacz_przymus_parkingu(self, v: bool):
        self.system.dane.czy_parking_musi_byc_darmowy = v != 0
        print(self.system.dane.czy_parking_musi_byc_darmowy, type(self.system.dane.czy_parking_musi_byc_darmowy))


    def wczytaj_baze(self, filename: Optional[str] = None):
        if not filename:
            filename = QtWidgets.QFileDialog.getOpenFileName(
                self, 'Wczytaj bazę z pliku...', None, 
                "Plik programu Excel (*.xlsx);;Plik CSV (*.csv)"
            )[0]
        if filename:
            try:
                baza = HotelLoader().zaladuj_plik(filename).jako_dataframe()
            except Exception as e:
                self.wyswietl_blad("Błąd wczytywania bazy danych", e)
                return
            self.plik_bazy = filename
            self.system.zaladuj_dane(baza)
            self.odswiez_dane_tabel()
            print(self.plik_bazy)
    

    def wyswietl_blad(self, label: str, exception: Exception):
        dialog = QtWidgets.QMessageBox()
        dialog.setWindowTitle(label)
        dialog.setText(f"{label}\n\n{str(exception)}")
        dialog.exec()