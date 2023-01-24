import pandas as pd
import numpy as np

import pathlib
import sys
p = str(pathlib.Path().absolute().joinpath("app/system_wyboru_hoteli").resolve())
if p not in sys.path:
    sys.path.insert(0, p)

from funkcje_rankingowe.rsm import ranking_rsm
# from app.system_wyboru_hoteli.funkcje_rankingowe.rsm import ranking_rsm


def test_rsm():
    """Test daje możliwość podstawowej weryfikacji kodu."""

    indeksy = [3, 6, 12]

    kryteria_hoteli = pd.DataFrame([
            (-2, 0),
            (1, -3),
            (0, -1)
        ], 
        index=indeksy,
        columns=[0, 1]
    )

    punkty_docelowe = np.array([
        [-1, 3],
        [0, 1],
        [2, 0],
    ])

    punkty_status_quo = np.array([
        [-2,0],
        [-1,-2],
        [0,-3],
    ])

    ranking = ranking_rsm(
        kryteria_hoteli,
        punkty_docelowe,
        punkty_status_quo
    )

    assert isinstance(ranking, pd.DataFrame), "Zwracany ranking nie jest DataFrame'm"

    ranking_indeksy = list(ranking.index)
    ranking_indeksy.sort()
    assert indeksy == ranking_indeksy, "Nie zachowano indeksowania z 'kryteria_hoteli'"
