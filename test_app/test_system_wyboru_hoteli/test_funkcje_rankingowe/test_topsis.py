import pandas as pd
import numpy as np

import pathlib
import sys
p = str(pathlib.Path().absolute().joinpath("app/system_wyboru_hoteli").resolve())
if p not in sys.path:
    sys.path.insert(0, p)

from funkcje_rankingowe.topsis import ranking_topsis


def test_topsis():
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

    ranking = ranking_topsis(
        kryteria_hoteli,
    )
    
    assert isinstance(ranking, pd.DataFrame), "Zwracany ranking nie jest DataFrame'm"

    ranking_indeksy = list(ranking.index).sort()
    assert indeksy == ranking_indeksy, "Nie zachowano indeksowania z 'kryteria_hoteli'"
