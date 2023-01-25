import sys
import pathlib
# Dodanie folderu src do ścieżki
p = str(pathlib.Path().absolute().joinpath("system_wyboru_hoteli").resolve())
if p not in sys.path:
    sys.path.insert(0, p)

from system_hoteli import SystemWyboruHoteli
import funkcje_rankingowe
from zapis_odczyt_rankingu import zapisz_ranking, wczytaj_ranking
from porownanie_rankingow import drawDistances as porownanie_rankingow