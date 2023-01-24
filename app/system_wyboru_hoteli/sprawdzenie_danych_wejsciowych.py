import numpy as np
import wstepne_przetwarzanie_kryteriow
import pandas as pd 

def czy_granice_kryteriow_sa_poprawne(
        wartosci_minimalne: np.ndarray, 
        wartosci_maksymalne: np.ndarray
    ) -> bool:
    """Sprawdza, czy podane granice kryteriów są poprawne.
    
    Funkcja otrzymuje dolne i górne wartości kryteriów wprowadzone przez użytkownika.
    Sprawdza, czy podane wartości zostały wpisane poprawnie (maks >= min).

    Parameters
    ----------
    wartosci_minimalne : np.ndarray
        Minimalne wartości kryteriów
    wartosci_maksymalne : np.ndarray
        Maksymalne wartości kryteriów
    
    Returns
    -------
    bool
        True, jeśli wartości granic kryteriów są poprawne, False w przeciwnym wypadku
    """

    return (wartosci_maksymalne >= wartosci_minimalne).all()


def czy_punkty_w_zbiorze_wzajemnie_niesprzeczne(
        zbior: np.ndarray
    ) -> bool:
    """Sprawdza, czy zbiór punktów jest wewnętrznie niesprzeczny.
    
    Użytkownik podając punkty status-quo lub docelowe, może nie zagwarantować, że te
    punkty są wzajemnie niesprzeczne. Funkcja sprawdza, czy tak jest.

    Parameters
    ----------
    zbior : np.ndarray
        Zbiór punktów do sprawdzenia
    
    Returns
    -------
    bool
        True, jeśli zbiór jest wzajemnie niesprzeczny, False w przeciwnym wypadku
    """
    niezdominowane = wstepne_przetwarzanie_kryteriow.wyznacz_punkty_niezdominowane(pd.DataFrame(zbior))

    if (len(niezdominowane) == len(zbior)):
        return True
    else:
        return False

    


def czy_zbiory_wzajemnie_niesprzeczne(zbior_lepszy: np.ndarray, zbior_gorszy: np.ndarray) -> bool:
    """Sprawdza, czy dwa zbiory punktów są wzajemnie niesprzeczne.
    
    Użytkownik podając punkty status-quo i docelowe, może nie zagwarantować, że te
    zbiory są wzajemnie niesprzeczne. Funkcja sprawdza, czy tak jest.

    Parameters
    ----------
    zbior_lepszy : np.ndarray
        Zbiór punktów z mniejszymi wartościami kryterialnymi (np. punkty docelowe)
    zbior_gorszy : np.ndarray
        Zbiór punktów z większymi wartościami kryterialnymi (np. punkty status-quo)
    
    Returns
    -------
    bool
        True, jeśli zbiory są wzajemnie niesprzeczne, False w przeciwnym wypadku
    """

    # TODO To tak nie działa!

    comb_sets = np.vstack([zbior_lepszy, zbior_gorszy])
    # for i in zbior_gorszy:
    #     comb_sets.append(i)
    niezdominowane = wstepne_przetwarzanie_kryteriow.wyznacz_punkty_niezdominowane(pd.DataFrame(comb_sets))
    niezdominowane = pd.DataFrame.to_numpy(niezdominowane) 
    if np.array_equal(niezdominowane,zbior_lepszy):
        return True
    else:
        return False
    
    return True


