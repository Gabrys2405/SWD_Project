from typing import Tuple, List
import csv
import pandas as pd
import wyjatki


def zapisz_ranking(plik: str, ranking: pd.DataFrame, metoda: str):
    # Ranking zawiera pierwszą kolumnę jako wartości rankingu

    wagi_rankingowe = ranking[ranking.columns[0]].copy(True)
    wagi_rankingowe.sort_index(inplace=True)
    # wagi_rankingowe.sort_values([wagi_rankingowe.columns[0]], inplace=True)
    pary_indeks_waga = zip(
        wagi_rankingowe.index, wagi_rankingowe.values
    )

    with open(plik, 'w', newline='', encoding='utf8') as file:
        writer = csv.writer(file)
        writer.writerow(('Indeks', f'Metoda {metoda}'))
        writer.writerows(pary_indeks_waga)


def wczytaj_ranking(plik: str) -> Tuple[pd.DataFrame, str]:
    with open(plik, 'r', newline='', encoding='utf8') as file:
        reader = iter(csv.reader(file))
        first_row = next(reader)

        indeksy: List[int] = []
        wartosci: List[float] = []
        for i_row, row in enumerate(reader):
            try:
                i = int(row[0])
                wartosc = float(row[1])
            except ValueError:
                raise ValueError(f"Konwersja wiersza {i_row+2} nieudana")
            indeksy.append(i)
            wartosci.append(wartosc)

        df = pd.DataFrame(wartosci, index=indeksy)
        return df, first_row[1]
