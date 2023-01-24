import numpy as np
import pandas as pd


"Implementacja tradycyjnej Topsis"

def ranking_topsis(
        kryteria_hoteli: pd.DataFrame,
        wagi: np.ndarray,
    ) -> pd.DataFrame:
    """Funkcja tworząca ranking metodą TOPSIS
    
    Parameters
    ----------
    kryteria_hoteli : pd.DataFrame
        DataFrame zawierający wyłącznie minimalizowane kryteria
    
    Returns
    -------
    pd.DataFrame
        DataFrame zawierający jedną kolumnę z wartościami rankingowymi, indeksowanymi
        jak w kryteria_hoteli
    """

    # TODO
    # Podpowiedzi:
    #  - kryteria_hoteli.values jest macierzą NumPy, zmiany w niej wpływają na DataFrame
    #  - kryteria_hoteli.drop(indeks) usuwa wiersz
    #  - kryteria_hoteli.index[i] zwraca indeks do użycia w metodzie drop()
    # Istotne jest, aby zachować pierwotne indeksowanie z kryteria_hoteli
    znormalizowane_kryteria = kryteria_hoteli / np.linalg.norm(kryteria_hoteli.astype(float), axis = 0)
    kryteria_z_wagami = znormalizowane_kryteria * wagi
    rozw_idealne = np.max(kryteria_z_wagami,axis=0)
    rozw_antyidealne = np.min(kryteria_z_wagami,axis=0)
    odl_od_idealnego = np.sqrt(np.sum((kryteria_z_wagami - rozw_idealne)**2,axis = 1).astype(float))
    odl_od_antyidealnego = np.sqrt(np.sum((kryteria_z_wagami - rozw_antyidealne) ** 2, axis=1).astype(float))
    ranking = odl_od_antyidealnego / (odl_od_antyidealnego + odl_od_idealnego)
    df = pd.DataFrame(ranking, index=kryteria_hoteli.index)
    df.sort_values([df.columns[0]], ascending=True)
    return df

"Implementacja funkcji Fuzzy Topsis"

def ranking_fuzzy_topsis(
    kryteria_hoteli: pd.DataFrame,
    wagi: np.ndarray,
    zysk_czy_koszt: np.ndarray
) -> pd.DataFrame:
    """Funkcja tworząca ranking metodą TOPSIS

        Parameters
        ----------
        kryteria_hoteli : pd.DataFrame
            DataFrame zawierający dane rozmyte hoteli

        wagi : np.ndarray
            Ndarray zwierający informacje o wadze danego kryterium

        zysk_czy_koszt : np.ndarray
            Ndarray zawierający informację czy dana kategoria zaliczana jest jako zysk czy koszt
            - Jeżeli True, to zysk
            -Jeżeli False, to koszt

        Returns
        -------
        pd.DataFrame
            DataFrame zawierający jedną kolumnę z wartościami rankingowymi, indeksowanymi
            jak w kryteria_hoteli
        """

    # TODO
    # Podpowiedzi:
    #  - kryteria_hoteli.values jest macierzą NumPy, zmiany w niej wpływają na DataFrame
    #  - kryteria_hoteli.drop(indeks) usuwa wiersz
    #  - kryteria_hoteli.index[i] zwraca indeks do użycia w metodzie drop()
    # Istotne jest, aby zachować pierwotne indeksowanie z kryteria_hoteli

    "Wyznaczanie punktów minimalnych i maksymalnych"
    a_minus = np.min(np.min(kryteria_hoteli,axis=0),axis=1)
    c_star = np.max(np.max(kryteria_hoteli,axis=0),axis=1)
    "Normalizacja macierzy i uwzględnienie wag"
    for i in range(kryteria_hoteli.shape[0]):
        for j in range(kryteria_hoteli.shape[1]):
            if zysk_czy_koszt[j]: kryteria_hoteli[i,j] = np.divide(kryteria_hoteli[i,j],c_star[j]) * wagi[j]
            else: kryteria_hoteli[i,j] = np.divide(a_minus[j],kryteria_hoteli[i,j]) * wagi[j]
    "Punkty idealne i antyidealne"
    a_star = np.max(np.max(kryteria_hoteli,axis=0),axis=1)
    a_minus = np.min(np.min(kryteria_hoteli,axis=0),axis=1)
    "Obliczanie odległości od punktów idealnych i antyidealnych"
    c = list()

    for i in range(kryteria_hoteli.shape[0]):
        dystans_minus,dystans_star = 0,0
        for j in range(kryteria_hoteli.shape[1]):
            dystans_minus += np.sum(np.power(kryteria_hoteli[i,j]-a_minus[j],2))/3
            dystans_star += np.sum(np.power(kryteria_hoteli[i,j]-a_star[j],2))/3
        c.append(np.sqrt(dystans_minus)/(np.sqrt(dystans_star)+np.sqrt(dystans_minus)))

    df = pd.DataFrame(c, index=kryteria_hoteli.index)
    df.sort_values([df.columns[0]], ascending=True)
    return df


