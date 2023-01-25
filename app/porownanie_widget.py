# Type Checking
from __future__ import annotations 
from typing import Optional, Callable, Any, Tuple, List
import io

# Real imports
from PySide6 import QtCore, QtWidgets, QtGui
import pandas as pd
import numpy as np
from table_models import DataFrameTableModel
from table_widget import EdiTableWidget

from system_wyboru_hoteli import SystemWyboruHoteli, wyjatki, wczytaj_ranking
from addons import get_default_font
from cache_pyplot_figures import execute_and_get_buffers
from system_wyboru_hoteli import porownanie_rankingow


class PorownanieWidget(QtWidgets.QWidget):


    def __init__(self):
        super().__init__()

        # [("ścieżka do pliku", "nazwa metody", ranking)]
        self._rankingi_do_porownania: List[Tuple[str, str, pd.DataFrame]] = []

        self._main_layout = QtWidgets.QVBoxLayout(self)
        # self._main_layout.setStretch(0, 1)
        # self._main_layout.setStretch(1, 2)
        self.setLayout(self._main_layout)

        self._layout_row_1 = QtWidgets.QVBoxLayout(self)
        self._main_layout.addLayout(self._layout_row_1, 3)
        self._layout_row_2 = QtWidgets.QVBoxLayout(self)
        self._main_layout.addLayout(self._layout_row_2, 7)


        element = QtWidgets.QLabel("Metody rankingowe do porównania", alignment=QtCore.Qt.AlignCenter)
        element.setFont(get_default_font())
        self._layout_row_1.addWidget(element)


        row = QtWidgets.QHBoxLayout()

        element = QtWidgets.QPushButton("Wczytaj ranking")
        element.clicked.connect(self.dodaj_ranking)
        row.addWidget(element)

        element = QtWidgets.QPushButton("Usuń ranking")
        element.pressed.connect(self.usun_ranking)
        row.addWidget(element)

        self.b_porownanie_rankingow = QtWidgets.QPushButton("Porównaj rankingi")
        element = self.b_porownanie_rankingow
        element.pressed.connect(self.porownaj_rankingi)
        element.setDisabled(True)
        row.addWidget(element)

        self._layout_row_1.addLayout(row)


        self.w_lista_rankingowa = QtWidgets.QListWidget()
        self.w_lista_rankingowa.setSelectionMode(QtWidgets.QListWidget.SelectionMode.SingleSelection)
        self._layout_row_1.addWidget(self.w_lista_rankingowa)


        element = QtWidgets.QLabel("Wynik porównań", alignment=QtCore.Qt.AlignHCenter)
        font = get_default_font()
        font.setBold(True)
        element.setFont(font)
        self._layout_row_2.addWidget(element)

        self.l_zgodne_wiersze = QtWidgets.QLabel("", alignment=QtCore.Qt.AlignHCenter)
        element = self.l_zgodne_wiersze
        font = get_default_font()
        font.setItalic(True)
        element.setFont(font)
        self._layout_row_2.addWidget(element)

        self._layout_wykresow = QtWidgets.QVBoxLayout()

        scroll_area = QtWidgets.QScrollArea()
        scroll_area.setAlignment(QtCore.Qt.AlignHCenter)
        self._widget_wykresow = QtWidgets.QWidget()
        self._widget_wykresow.setLayout(self._layout_wykresow)
        scroll_area.setWidget(self._widget_wykresow)
        self._layout_row_2.addWidget(scroll_area)

        self._odswiez_ploty([])


    def porownaj_rankingi(self):
        if len(self._rankingi_do_porownania) < 2:
            self.wyswietl_blad("Błąd generowania porównania", wyjatki.BladDanychUzytkownika("Za mało rankingów do porównania"))
            return

        nazwy_rankingow = [f"{i}: {t}" for i, (_, t, _) in enumerate(self._rankingi_do_porownania)]
        rankingi = [t for _, _, t in self._rankingi_do_porownania]

        # wykonaj inner join na indeksach
        indeksy = set(rankingi[0].index)
        for ir in range(1, len(rankingi)):
            indeksy.intersection_update(rankingi[ir].index)
        
        indeksy = list(indeksy)
        if len(indeksy) < 1:
            self.wyswietl_blad("Błąd generowania porównania", wyjatki.BladDanychUzytkownika("Rankingi nie mają wspólnych wierszy"))
            return
        self.l_zgodne_wiersze.setText(f"Zgodne wiersze: {len(indeksy)}")

        # print(f"{indeksy = }")

        # Przepisz nowe rankingi z wyłącznie wspólnymi indeksami
        for ir in range(len(rankingi)):
            rankingi[ir]: pd.DataFrame = rankingi[ir].loc[indeksy]
            # print(f"{rankingi[ir] = }")

        try:
            # Wyłap ploty utworzone podczas generowania porównania
            imgs, _ = execute_and_get_buffers(lambda: porownanie_rankingow(nazwy_rankingow, rankingi))
        except Exception as e:
            # Wyłap błędy przetwarzania od użytkownika
            self.wyswietl_blad("Błąd poprawności danych", e)
            raise e

        self._odswiez_ploty(imgs)


    def dodaj_ranking(self, filename: Optional[str] = None):
        if not filename:
            filename = QtWidgets.QFileDialog.getOpenFileName(
                self, 'Wczytaj ranking z pliku...', None, 
                "Plik CSV (*.csv)"
            )[0]
        if filename:
            try:
                ranking, metoda = wczytaj_ranking(filename)
            except Exception as e:
                self.wyswietl_blad("Błąd oczytu rankingu", e)
                raise e
            self._rankingi_do_porownania.append((filename, metoda, ranking))
            self.w_lista_rankingowa.addItem(f"{metoda} - {filename}")
            self.b_porownanie_rankingow.setDisabled(len(self._rankingi_do_porownania) < 2)


    def usun_ranking(self):
        zaznaczone: List[QtCore.QModelIndex] = self.w_lista_rankingowa.selectedIndexes()
        print(f"{zaznaczone = }, {type(zaznaczone) = }")
        if len(zaznaczone) == 1:
            indeks = zaznaczone[0].row()
            self.w_lista_rankingowa.takeItem(indeks)
            self._rankingi_do_porownania.pop(indeks)
            self.b_porownanie_rankingow.setDisabled(len(self._rankingi_do_porownania) < 2)


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