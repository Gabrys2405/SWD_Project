import sys
import pathlib
# Dodanie folderu src do ścieżki
p = str(pathlib.Path().absolute().joinpath("system_wyboru_hoteli").resolve())
if p not in sys.path:
    sys.path.insert(0, p)

from system_hoteli import SystemWyboruHoteli
import funkcje_rankingowe