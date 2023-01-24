
import csv
import pandas as pd


def zapisz_ranking(plik: str, ranking: pd.DataFrame, metoda: str):
    # Ranking zawiera pierwszą kolumnę jako wartości rankingu

    wagi_rankingowe = ranking[ranking.columns[0]].copy(True)
    wagi_rankingowe.sort_index(inplace=True)
    # wagi_rankingowe.sort_values([wagi_rankingowe.columns[0]], inplace=True)
    pary_indeks_waga = zip(
        wagi_rankingowe.index, wagi_rankingowe.values
    )

    with open(plik, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(('Indeks', f'Metoda {metoda}'))
        writer.writerows(pary_indeks_waga)
