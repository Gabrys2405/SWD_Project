# Autor główny: Piotr Sikorski
from __future__ import annotations 
from typing import Dict, Optional, List, Literal
import numpy as np
import pandas as pd
import wyjatki
import sprawdzenie_danych_wejsciowych
import wstepne_przetwarzanie_kryteriow
import funkcje_rankingowe
from zbior_danych import ZbiorDanych


class SystemWyboruHoteli():
    """Klasa zbierająca funkcjonalność systemu wyboru hoteli.
    
    Klasa zbiera w jednym miejscu całe przetwarzanie danych koniecznych do 
    wyboru odpowiedniego hotelu. Zawiera metody przetwarzające i przechowuje
    wyniki działań.
    """

    def __init__(self) -> None:
        # Oryginalne dane systemu, tworzone podczas ładowania bazy
        self.dane: Optional[ZbiorDanych] = None

        # Modyfikowane dane podczas tworzenia rankingów
        # Zawierają tylko kolumny wybrane przez użytkownika
        self._dane_przetwarzane: Optional[ZbiorDanych] = None

        # === Wyniki === #
        # Słownik mapujący nazwę metody do jej rankingu
        self.rankingi_metod: Optional[Dict[str, pd.DataFrame]] = None
        pass


    def zaladuj_dane(self, dane_hoteli: pd.DataFrame):
        """Tworzy DataFrame'y na podstawie danych hoteli"""
        self.dane = ZbiorDanych(dane_hoteli)
        

    def _sprawdz_poprawnosc_danych(self):

        # Sprawdzenie poprawności danych systemowo

        # Czy wprowadzono w ogóle dane?
        nazwy_parametrow: List[str] = [
            "dane_hoteli", "wybrane_kryteria", "minimalne_kryteria", "maksymalne_kryteria",
            "punkty_docelowe", "punkty_status_quo"
        ]
        for nazwa in nazwy_parametrow:
            if getattr(self.dane, nazwa) is None:
                raise wyjatki.BrakInicjalizacjiParametru(nazwa)
    
        # Szerokości macierzy
        szerokosc_oczekiwana: int = self.dane.kryteria_hoteli.shape[1]
        nazwy_parametrow: List[str] = [
            "wybrane_kryteria", "minimalne_kryteria", "maksymalne_kryteria",
            "punkty_docelowe", "punkty_status_quo"
        ]
        for nazwa in nazwy_parametrow:
            szerokosc: int = getattr(self.dane, nazwa).shape[1]
            if szerokosc != szerokosc_oczekiwana:
                raise wyjatki.NiepoprawnaSzerokoscMacierzy(nazwa, szerokosc, szerokosc_oczekiwana)
        

        # Sprawdzanie danych użytkownika

        # Wybrano co najmniej jedno kryterium
        if np.sum(self.dane.wybrane_kryteria.values.astype("int")) < 1:
            raise wyjatki.BladDanychUzytkownika("Wybrano za małą ilość kryteriów")


        # W tym miejscu możesz wybrać tylko kolumny wybrane przez użytkownika
        self._dane_przetwarzane = self.dane.kopia_z_wybranymi_kryteriami()
        dane = self._dane_przetwarzane

        # Punkty docelowe i status-quo muszą być zmienione na minimalizację!
        dane.punkty_docelowe = wstepne_przetwarzanie_kryteriow.zamien_maksymalizacje_na_minimalizacje(
            dane.punkty_docelowe, dane.kolumny_maks_na_min__lista
        )
        dane.punkty_status_quo = wstepne_przetwarzanie_kryteriow.zamien_maksymalizacje_na_minimalizacje(
            dane.punkty_status_quo, dane.kolumny_maks_na_min__lista
        )

        # Granice kryteriów
        if not sprawdzenie_danych_wejsciowych.czy_granice_kryteriow_sa_poprawne(
            dane.minimalne_kryteria.values, 
            dane.maksymalne_kryteria.values
        ):
            raise wyjatki.BladDanychUzytkownika("Kryteria minimalne i maksymalne są sprzeczne")
        
        # Niesprzeczności zbiorów
        if not sprawdzenie_danych_wejsciowych.czy_punkty_w_zbiorze_wzajemnie_niesprzeczne(
            dane.punkty_docelowe.values
        ):
            raise wyjatki.BladDanychUzytkownika("Punkty w zbiorze punktów docelowych są wzajemnie sprzeczne")
        if not sprawdzenie_danych_wejsciowych.czy_punkty_w_zbiorze_wzajemnie_niesprzeczne(
            dane.punkty_status_quo.values
        ):
            raise wyjatki.BladDanychUzytkownika("Punkty w zbiorze punktów status-quo są wzajemnie sprzeczne")
        if not sprawdzenie_danych_wejsciowych.czy_zbiory_wzajemnie_niesprzeczne(
            dane.punkty_docelowe.values, 
            dane.punkty_status_quo.values
        ):
            raise wyjatki.BladDanychUzytkownika("Zbiory punktów docelowych i status-quo są wzajemnie sprzeczne") 

        # Wszystko poprawne
        return
    

    def _wykonaj_przetwarzanie_kryteriow(self):
        dane = self._dane_przetwarzane
        kryteria_hoteli = dane.kryteria_hoteli

        kryteria_hoteli = wstepne_przetwarzanie_kryteriow.filtruj_hotele__czy_parking_darmowy(
            dane.dane_hoteli, kryteria_hoteli, dane.czy_parking_musi_byc_darmowy
        )

        kryteria_hoteli = wstepne_przetwarzanie_kryteriow.filtruj_hotele__wartosci_kryteriow_minimalne_i_maksymalne(
            kryteria_hoteli, dane.minimalne_kryteria.values, dane.maksymalne_kryteria.values
        )

        kryteria_hoteli = wstepne_przetwarzanie_kryteriow.zamien_maksymalizacje_na_minimalizacje(
            kryteria_hoteli, dane.kolumny_maks_na_min__lista
        )

        kryteria_hoteli = wstepne_przetwarzanie_kryteriow.wyznacz_punkty_niezdominowane(
            kryteria_hoteli
        )

        self._dane_przetwarzane.kryteria_hoteli = kryteria_hoteli
    

    def wygeneruj_ranking(self, nazwa_metody: Literal["topsis", "rsm"]) -> pd.DataFrame:
        """Metoda zwracająca dane jednego, wybranego rankingu.
        
        Metoda sprawdza i przetwarza zapisane wcześniej dane, i zwraca
        DataFrame zawierający ranking danych wg wybranej metody.
        """

        self._sprawdz_poprawnosc_danych()
        self._wykonaj_przetwarzanie_kryteriow()

        dane = self._dane_przetwarzane
        if nazwa_metody == "topsis":
            ranking = funkcje_rankingowe.ranking_topsis(
                dane.kryteria_hoteli
            )
        elif nazwa_metody == "rsm":
            ranking = funkcje_rankingowe.ranking_rsm(
                dane.kryteria_hoteli, 
                dane.punkty_docelowe.values,
                dane.punkty_status_quo.values
            )
        else:
            raise KeyError(f"Nie znaleziono metody rankingowej o nazwie '{nazwa_metody}'")

        # Sortuj ranking rosnąco
        ranking.sort_values(ranking.columns[0])
        # Zmień nazwę kolumny rankingowej
        ranking.rename(columns={ranking.columns[0]:"Wartość rankingu"}, inplace=True)
        # Uzupełnij ranking o wartości z bazy
        ranking = pd.concat([ranking, self._dane_przetwarzane.dane_hoteli], axis=1, join='inner')

        return ranking
