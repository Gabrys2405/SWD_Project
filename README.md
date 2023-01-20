# SWD_Project

## Instalacja środowiska Conda

Pakiety będą zmieniać się wraz z rozwojem aplikacji.

Poniższe polecenie można użyć również na istniejącym środowisku w celu doinstalowania / aktualizacji pakietów.

```PowerShell
conda install --file .\conda_dependencies.txt -c conda-forge -n (nazwa_srodowiska)
```

## Schemat logiki biznesowej aplikacji

Schemat przetwarzania informacji przez aplikację (bez GUI, moduł [system_wyboru_hoteli](app/system_wyboru_hoteli)):

* inicjalizacja klasy _SystemWyboruHoteli_ ([system_wyboru_hoteli.py](app/system_wyboru_hoteli/system_wyboru_hoteli.py)) i uzupełnienie o dane użytkownika,
* wykonanie wybranego rankingu:
    * sprawdzenie danych wprowadzonych przez użytkownika - zgłaszanie wyjątków ([sprawdzenie_danych_wejsciowych.py](app/system_wyboru_hoteli/sprawdzenie_danych_wejsciowych.py)),
    * wykonanie wstępnych operacji (np. filtrowania) na danych ([wstepne_przetwarzanie_kryteriow.py](app/system_wyboru_hoteli/wstepne_przetwarzanie_kryteriow.py)),
    * wykonanie rankingu wybranej metody (moduł [funkcje_rankingowe](app/system_wyboru_hoteli/funkcje_rankingowe));
* zwrócenie wyników.

Klasa _SystemWyboruHoteli_ **nie** ładuje danych z pliku, lecz otrzymuje DataFrame z danymi. Ładowanie danych jest obsługiwane przez GUI z użyciem pliku [hotel_loader.py](app/hotel_loader.py).


## Uzupełnianie metod

**Do uzupełnienia jest wiele metod oznaczonych _# TODO_.**

W środku funkcji można tworzyć wykresy za pomocą *matplotlib.pyplot*, a następnie wyświetlać je w oknie programu po prostu wywołując *matplotlib.pyplot.show()*
