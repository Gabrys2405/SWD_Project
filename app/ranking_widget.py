# Type Checking
from __future__ import annotations 
from typing import Optional, Callable, Any, Tuple, List
import io

# Real imports
from PySide6 import QtCore, QtWidgets, QtGui
import pandas as pd
from table_models import DataFrameTableModel
from table_widget import EdiTableWidget

from system_wyboru_hoteli import SystemWyboruHoteli, wyjatki, zapisz_ranking
from addons import get_default_font
from cache_pyplot_figures import execute_and_get_buffers


class RankingWidget(QtWidgets.QWidget):

    _metody_rankingowe: List[Tuple[str, str]] = [
        ("topsis", "TOPSIS"),
        ("fuzzy_topsis", "Fuzzy TOPSIS"),
        ("rsm", "RSM"),
        ("safety_principle", "Safety Principle"),
    ]

    def __init__(self, system: SystemWyboruHoteli):
        super().__init__()
        self.system = system
        self._obecny_ranking: Optional[pd.DataFrame] = None
        self._obecna_metoda: int = -1

        self._main_layout = QtWidgets.QHBoxLayout(self)
        # self._main_layout.setStretch(0, 1)
        # self._main_layout.setStretch(1, 2)
        self.setLayout(self._main_layout)

        self._layout_column_1 = QtWidgets.QVBoxLayout(self)
        self._main_layout.addLayout(self._layout_column_1, 2)
        self._layout_column_2 = QtWidgets.QVBoxLayout(self)
        self._main_layout.addLayout(self._layout_column_2, 1)


        # LEWA KOLUMNA

        row = QtWidgets.QHBoxLayout()

        element = QtWidgets.QLabel("Metoda rankingowa", alignment=QtCore.Qt.AlignCenter)
        element.setFont(get_default_font())
        row.addWidget(element)

        self.w_lista_metod = QtWidgets.QComboBox()
        element = self.w_lista_metod
        for _, nazwa_metody in self._metody_rankingowe:
            element.addItem(nazwa_metody)
        element.currentIndexChanged.connect(lambda s: print(s))
        row.addWidget(element)

        element = QtWidgets.QPushButton("Wygeneruj ranking")
        element.pressed.connect(self.wyswietl_ranking)
        row.addWidget(element)

        self.b_zapisz_ranking = QtWidgets.QPushButton("Zapisz wygenerowany ranking")
        element = self.b_zapisz_ranking
        element.pressed.connect(self.zapisz_ranking)
        element.setDisabled(True)
        row.addWidget(element)

        self._layout_column_1.addLayout(row)

        self.l_ranking = QtWidgets.QLabel("Nie utworzono rankingu", alignment=QtCore.Qt.AlignHCenter)
        element = self.l_ranking
        font = get_default_font()
        font.setBold(True)
        element.setFont(font)
        self._layout_column_1.addWidget(element)

        table_widget = EdiTableWidget()
        self.t_ranking = table_widget
        self._layout_column_1.addWidget(table_widget)


        # PRAWA KOLUMNA

        element = QtWidgets.QLabel("Wykresy wynikowe", alignment=QtCore.Qt.AlignHCenter)
        font = get_default_font()
        font.setBold(True)
        element.setFont(font)
        self._layout_column_2.addWidget(element)

        self._layout_wykresow = QtWidgets.QVBoxLayout()

        scroll_area = QtWidgets.QScrollArea()
        self._widget_wykresow = QtWidgets.QWidget()
        self._widget_wykresow.setLayout(self._layout_wykresow)
        scroll_area.setWidget(self._widget_wykresow)
        self._layout_column_2.addWidget(scroll_area)

        self._odswiez_ploty([])


    def wyswietl_ranking(self):
        indeks_metody = self.w_lista_metod.currentIndex()
        id_metody, nazwa_metody = self._metody_rankingowe[indeks_metody]

        try:
            # Wyłap ploty utworzone podczas generowania rankingu
            imgs, ranking = execute_and_get_buffers(lambda: self.system.wygeneruj_ranking(id_metody))
        except Exception as e:
            # Wyłap błędy przetwarzania od użytkownika
            self.wyswietl_blad("Błąd poprawności danych", e)
            raise e
        
        self._obecny_ranking = ranking
        self._obecna_metoda = indeks_metody
        self.b_zapisz_ranking.setDisabled(False)

        # Wgraj ranking do tabeli
        model = DataFrameTableModel(ranking)
        self.t_ranking.setModel(model)
        h = self.t_ranking.horizontalHeader()
        for i, _ in enumerate(ranking.columns):
            h.setSectionResizeMode(i, QtWidgets.QHeaderView.ResizeMode.Stretch)

        self._odswiez_ploty(imgs)

        self.l_ranking.setText(f"Ranking dla metody {nazwa_metody}")


    def zapisz_ranking(self, filename: Optional[str] = None):
        if not filename:
            filename = QtWidgets.QFileDialog.getSaveFileName(
                self, 'Zapisz ranking do pliku...', None, 
                "Plik CSV (*.csv)"
            )[0]
        if filename:
            try:
                zapisz_ranking(filename, self._obecny_ranking, self._metody_rankingowe[self._obecna_metoda][1])
            except Exception as e:
                self.wyswietl_blad("Błąd zapisu rankingu", e)
                raise e


    def _odswiez_ploty(self, img_bufs: List[io.BytesIO]):
        # Usuń poprzednie ploty
        # for w in reversed(self._layout_wykresow.children()):
        #     w.setParent(None)
        for i in reversed(range(self._layout_wykresow.count())): 
            self._layout_wykresow.itemAt(i).widget().setParent(None)

        if len(img_bufs) == 0:
            # Brak plotów
            element = QtWidgets.QLabel("Brak wykresów", alignment=QtCore.Qt.AlignCenter)
            font = get_default_font()
            font.setItalic(True)
            element.setFont(font)
            self._layout_wykresow.addWidget(element)
            self._widget_wykresow.setFixedSize(element.width(), element.height())
        else:
            # Wyświetl nowe ploty
            width = 0
            height = 0
            for img_buf in img_bufs:
                q_img: QtGui.QImage = QtGui.QImage.fromData(QtCore.QByteArray(img_buf.getvalue()))
                element = QtWidgets.QLabel("", alignment=QtCore.Qt.AlignCenter)
                element.setPixmap(QtGui.QPixmap(q_img))
                self._layout_wykresow.addWidget(element)
                height += element.height()
                width = max(width, element.width())
            self._widget_wykresow.setFixedSize(width, height)


    def wyswietl_blad(self, label: str, exception: Exception):
        dialog = QtWidgets.QMessageBox()
        dialog.setWindowTitle(label)
        dialog.setText(f"{label}\n\n{str(exception)}")
        dialog.exec()