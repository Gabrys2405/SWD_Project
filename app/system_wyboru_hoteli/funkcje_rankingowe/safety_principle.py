import numpy as np
import pandas as pd
from typing import List, Tuple

def odleglosc_od_odcinka(x, p1, p2) -> Tuple[float, float]:
    # Zwraca odległość punktu od odcinka oraz w jakiej części odcinka się znajduje

    # Odległości między punktami
    p1x = np.sqrt(np.sum(np.square(p1 - x)))
    p2x = np.sqrt(np.sum(np.square(p2 - x)))
    p1p2 = np.sqrt(np.sum(np.square(p1 - p2)))

    # Jeśli któryś bok jest zerowy, punkt leży dokładnie na którymś z punktów
    if p1x == 0:
        return 0, 0
    if p2x == 0:
        return 0, 1
        
    # Jeśli punkty są jednakowe, zwróć odległość od punktu
    if p1p2 == 0:
        return p1x, 0

    # Kąt przy punkcie p1 i p2
    # min() - błędy float powodują, że czasem wartość kąta jest większa od 1
    sq1 = (np.square(p1p2) + np.square(p1x) - np.square(p2x))/(2*p1p2*p1x)
    alfa1 = np.arccos(min(max(sq1, -1), 1))

    sq2 = (np.square(p1p2) + np.square(p2x) - np.square(p1x))/(2*p1p2*p2x)
    alfa2 = np.arccos(min(max(sq2, -1), 1))


    # Sprawdzenie czy punkt x rzutuje na odcinek |p1 p2|
    if alfa1 >= np.pi/2:
        return p1x, 0
    elif alfa2 >= np.pi/2:
        return p2x, 1
    else:   # Punkt x rzutuje na odcinek |p1 p2| (rzut oznaczony punktem d)
        h = p1x * np.sin(alfa1)  # odległość x od odcinka
        dp1 = np.sqrt(np.square(p1x) - np.square(h))  # odległość d od p1
        return h, dp1 / p1p2
        
class KrzywaWoronoja():
    def __init__(self, p1: np.ndarray, p2: np.ndarray) -> None:
        assert len(p1.shape) == len(p2.shape) == 1; "Zły wymiar macierzy punktu"
        assert p1.shape[0] == p2.shape[0]; "Wymiary punktów niezgodne"

        self.wymiar = p1.shape[0]

        self.p1: np.ndarray = p1.astype('float')
        self.p2: np.ndarray = p2.astype('float')

        self.p_srodkowy = (self.p1+self.p2)/2

        # zawierają punkty pi oraz środkowy
        self.punkty_lamanej_od_p1: np.ndarray = np.zeros((self.wymiar+1, self.wymiar))
        self.punkty_lamanej_od_p2: np.ndarray = np.zeros((self.wymiar+1, self.wymiar))

        self.minimalne_odleglosci: np.ndarray = np.zeros((self.wymiar,))
        self.dlugosci_krzywej: np.ndarray = np.zeros((self.wymiar,))  # Długości połowy krawędzi
        self.dlugosc_krzywej: float = 0

        self.wyznacz_lamana()
    
    def wyznacz_lamana(self):
        # transponuj punkty do początku układu współrzędnych, czyli p1 = 0
        p1 = np.zeros((self.wymiar))
        p2 = self.p2 - self.p1
        # p_srodkowy = self.p_srodkowy - self.p1
        odleglosci = np.abs(p2)

        # Weż najmniejszą długość boku, odejmij od innych długości, podziel przez 2 a następnie dodaj do 
        # poprzedniego punktu łamanej
        # self.punkty_lamanej_od_p1[0, :] = 0
        self.punkty_lamanej_od_p2[0, :] = p2

        # print(f"{odleglosci = }")

        for i in range(1, self.wymiar+1):
            i_min_odl = np.argmin(odleglosci)
            minimalna_odleglosc = odleglosci[i_min_odl]
            # print(f"{minimalna_odleglosc = }")
            odleglosci -= minimalna_odleglosc
            self.minimalne_odleglosci[i-1] = minimalna_odleglosc
            self.dlugosci_krzywej[i-1] = minimalna_odleglosc * np.sqrt(self.wymiar-i+1) / 2

            delta_odleglosci = minimalna_odleglosc / 2 * (odleglosci != np.inf).astype('int')  # nie uwzględniaj zerowych ścian

            self.punkty_lamanej_od_p1[i] = self.punkty_lamanej_od_p1[i-1] + delta_odleglosci
            self.punkty_lamanej_od_p2[i] = self.punkty_lamanej_od_p2[i-1] - delta_odleglosci

            odleglosci[i_min_odl] = np.inf  # nie uwzględniaj w następnych iteracjach - ściana ma zero

        # transponuj z powrotem
        self.punkty_lamanej_od_p1 += self.p1
        self.punkty_lamanej_od_p2 += self.p1
        self.dlugosc_krzywej = np.sum(self.dlugosci_krzywej) * 2
    

    def pozycja_na_krzywej(self, x: np.ndarray) -> float:
        # Dla każdego odcinka łamanej wylicz odległość i wybierz najmniejszą
        # Policz pozycję na krzywej (0, 1) i zwróć
        d_min: float = np.inf
        suma_dlugosci_lamanej_min: float = 0

        suma_dlugosci_lamanej: float = 0

        for i in range(self.punkty_lamanej_od_p1.shape[0] - 1):
            p1 = self.punkty_lamanej_od_p1[i]
            p2 = self.punkty_lamanej_od_p1[i+1]
            odl, dl_rzutowana = odleglosc_od_odcinka(x, p1, p2)
            if odl < d_min:
                d_min = odl
                suma_dlugosci_lamanej_min = suma_dlugosci_lamanej + dl_rzutowana * self.dlugosci_krzywej[i]
            suma_dlugosci_lamanej += self.dlugosci_krzywej[i]
        
        for i in reversed(range(self.punkty_lamanej_od_p2.shape[0] - 1)):
            p2 = self.punkty_lamanej_od_p2[i]
            p1 = self.punkty_lamanej_od_p2[i+1]
            odl, dl_rzutowana = odleglosc_od_odcinka(x, p1, p2)
            if odl < d_min:
                d_min = odl
                suma_dlugosci_lamanej_min = suma_dlugosci_lamanej + dl_rzutowana * self.dlugosci_krzywej[i]
            suma_dlugosci_lamanej += self.dlugosci_krzywej[i]

        return suma_dlugosci_lamanej_min / self.dlugosc_krzywej


def ranking_safety_principle(
        kryteria_hoteli: pd.DataFrame,
        punkty_docelowe: np.ndarray,
        punkty_status_quo: np.ndarray
    ) -> pd.DataFrame:
    """Funkcja tworząca ranking metodą Safety Principle
    
    Parameters
    ----------
    kryteria_hoteli : pd.DataFrame
        DataFrame zawierający wyłącznie minimalizowane kryteria
    punkty_docelowe : np.ndarray
        Punkty docelowe dla metody SP
    punkty_status_quo : np.ndarray
        Punkty status-quo dla metody SP
    
    Returns
    -------
    pd.DataFrame
        DataFrame zawierający jedną kolumnę z wartościami rankingowymi, indeksowanymi
        jak w kryteria_hoteli, posortowana względem jakości rankingu (najlepsze jako pierwsze)
    """

    krzywe_Woronoja: List[KrzywaWoronoja] = []
    for ia0 in range(punkty_status_quo[0]):
        a0 = punkty_status_quo[ia0, :]
        for ia1 in range(punkty_docelowe.shape[0]):
            a1 = punkty_docelowe[ia1, :]
            krzywe_Woronoja.append(KrzywaWoronoja(a1, a0))
            
    ranking: np.ndarray = np.zeros((kryteria_hoteli[0], 2))
    
    for ia in range(kryteria_hoteli[0]):
        a = kryteria_hoteli[ia, :]
        suma_poz: float = 0
        for k in krzywe_Woronoja:
            suma_poz += k.pozycja_na_kzywej(a)
        ranking[ia, 0] = ia + 1
        ranking[ia, 1] = suma_poz
    
    rank = pd.DataFrame(ranking, index = kryteria_hoteli.index)
    rank.sort_values(rank.columns)
    
    return rank
            
            

