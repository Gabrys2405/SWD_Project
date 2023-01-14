# Autor główny: Piotr Sikorski

from typing import Dict, Optional, List
import numpy as np
import pandas as pd
import wyjatki
import sprawdzenie_danych_wejsciowych
import wstepne_przetwarzanie_kryteriow
import funkcje_rankingowe


def indeksy_na_kolumny(df: pd.DataFrame, indeksy: List[int]) -> pd.Index:
    return [df.columns[i] for i in indeksy]


class SystemWyboruHoteli():
    """Klasa zbierająca funkcjonalność systemu wyboru hoteli.
    
    Klasa zbiera w jednym miejscu całe przetwarzanie danych koniecznych do 
    wyboru odpowiedniego hotelu. Zawiera metody przetwarzające i przechowuje
    wyniki działań.
    """

    # Indeksy kolumn, które zawierają dane kryterialne
    kolumny_kryteriow: List[int] = [2, 3, 4, 5, 7]


    def __init__(self) -> None:
        # === Parametry === #

        # Dane wszystkich hoteli
        self.dane_hoteli: Optional[pd.DataFrame] = None

        self.minimalne_kryteria: Optional[np.ndarray] = None
        self.maksymalne_kryteria: Optional[np.ndarray] = None

        self.punkty_docelowe: Optional[np.ndarray] = None
        self.punkty_status_quo: Optional[np.ndarray] = None

        self.czy_parking_musi_byc_darmowy: bool = False


        # === Cache === #

        # DataFrame zawierający wyłacznie kryteria pasujących 
        # i niezdominowanych hoteli 
        self.kryteria_hoteli: Optional[pd.DataFrame] = None


        # === Wyniki === #

        # Słownik mapujący nazwę metody do jej rankingu
        self.rankingi_metod: Optional[Dict[str, pd.DataFrame]] = None
        pass


    def wykonaj_wszystkie_obliczenia(self) -> None:
        """Funkcja wykonująca wszystkie kalkulacje do rankingów.

        Funkcja przetwarza wcześniej wprowadzone do niej dane, aby zapisać
        w sobie rankingi z nich wynikające. Zgłasza wiele wyjątków, najczęściej 
        dla niepoprawnych danych. 
        """

        self._sprawdz_poprawnosc_danych()
        self._wykonaj_przetwarzanie_kryteriow()
        self._wygeneruj_rankingi()


    def _sprawdz_poprawnosc_danych(self):

        # Czy wprowadzono w ogóle dane?
        nazwy_parametrow: List[str] = [
            "dane_hoteli", "minimalne_kryteria", "maksymalne_kryteria",
            "punkty_docelowe", "punkty_status_quo"
        ]
        for nazwa in nazwy_parametrow:
            if getattr(self, nazwa) is None:
                raise wyjatki.BrakInicjalizacjiParametru(nazwa)
        
        
        # Można utworzyć macierz z samymi kryteriami
        kolumny = indeksy_na_kolumny(self.dane_hoteli, self.kolumny_kryteriow)
        self.kryteria_hoteli = self.dane_hoteli[kolumny]


        # Sprawdzenie poprawności danych

        # Szerokości macierzy
        szerokosc_oczekiwana: int = self.kryteria_hoteli.shape[1]
        nazwy_parametrow: List[str] = [
            "minimalne_kryteria", "maksymalne_kryteria",
            "punkty_docelowe", "punkty_status_quo"
        ]
        for nazwa in nazwy_parametrow:
            szerokosc: int = getattr(self, nazwa).shape[1]
            if szerokosc != szerokosc_oczekiwana:
                raise wyjatki.NiepoprawnaSzerokoscMacierzy(nazwa, szerokosc, szerokosc_oczekiwana)
        
        # Granice kryteriów
        if not sprawdzenie_danych_wejsciowych.czy_granice_kryteriow_sa_poprawne(
            self.minimalne_kryteria, self.maksymalne_kryteria
        ):
            raise wyjatki.BladDanychUzytkownika("Kryteria minimalne i maksymalne są sprzeczne")
        
        # Niesprzeczności zbiorów
        if not sprawdzenie_danych_wejsciowych.czy_punkty_w_zbiorze_wzajemnie_niesprzeczne(
            self.punkty_docelowe
        ):
            raise wyjatki.BladDanychUzytkownika("Punkty w zbiorze punktów docelowych są wzajemnie sprzeczne")
        if not sprawdzenie_danych_wejsciowych.czy_punkty_w_zbiorze_wzajemnie_niesprzeczne(
            self.punkty_status_quo
        ):
            raise wyjatki.BladDanychUzytkownika("Punkty w zbiorze punktów status-quo są wzajemnie sprzeczne")
        if not sprawdzenie_danych_wejsciowych.czy_zbiory_wzajemnie_niesprzeczne(
            self.punkty_docelowe, self.punkty_status_quo
        ):
            raise wyjatki.BladDanychUzytkownika("Zbiory punktów docelowych i status-quo są wzajemnie sprzeczne") 

        # Wszystko poprawne
        return
    

    def _wykonaj_przetwarzanie_kryteriow(self):
        kryteria_hoteli = self.kryteria_hoteli

        kryteria_hoteli = wstepne_przetwarzanie_kryteriow.filtruj_hotele__czy_parking_darmowy(
            self.dane_hoteli, kryteria_hoteli, self.czy_parking_musi_byc_darmowy
        )

        kryteria_hoteli = wstepne_przetwarzanie_kryteriow.filtruj_hotele__wartosci_kryteriow_minimalne_i_maksymalne(
            kryteria_hoteli, self.minimalne_kryteria, self.maksymalne_kryteria
        )

        kryteria_hoteli = wstepne_przetwarzanie_kryteriow.zamien_maksymalizacje_na_minimalizacje(
            kryteria_hoteli
        )

        kryteria_hoteli = wstepne_przetwarzanie_kryteriow.wyznacz_punkty_niezdominowane(
            kryteria_hoteli
        )

        self.kryteria_hoteli = kryteria_hoteli
    

    def _wygeneruj_rankingi(self):
        self.rankingi_metod = {
            'topsis': funkcje_rankingowe.ranking_topsis(
                self.kryteria_hoteli
            ),
            'rsm': funkcje_rankingowe.ranking_rsm(
                self.kryteria_hoteli, self.punkty_docelowe, self.punkty_status_quo
            )
        }