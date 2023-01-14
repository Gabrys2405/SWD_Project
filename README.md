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
* wykonanie rankingów:
    * sprawdzenie danych wprowadzonych przez użytkownika - zgłaszanie wyjątków ([sprawdzenie_danych_wejsciowych.py](app/system_wyboru_hoteli/sprawdzenie_danych_wejsciowych.py)),
    * wykonanie wstępnych operacji (np. filtrowania) na danych ([wstepne_przetwarzanie_kryteriow.py](app/system_wyboru_hoteli/wstepne_przetwarzanie_kryteriow.py)),
    * wykonanie rankingów poszczególnych metod (moduł [funkcje_rankingowe](app/system_wyboru_hoteli/funkcje_rankingowe)),
    * porównanie rankingów;
* zapisanie wyników w klasie.

Klasa _SystemWyboruHoteli_ **nie** ładuje danych z pliku, lecz otrzymuje DataFrame z danymi. *Ładowanie danych najpewniej będzie znajdowało się w niezależnym pliku hotel_loader.py.* 

*Klasa ta będzie obsługiwana przez GUI.*

**Do uzupełnienia jest wiele metod oznaczonych _# TODO_.**