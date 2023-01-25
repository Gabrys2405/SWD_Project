# SWD_Project

## Instrukcje instalacji

### Instalacja środowiska Conda

Pakiety będą zmieniać się wraz z rozwojem aplikacji.

Poniższe polecenie można użyć również na istniejącym środowisku w celu doinstalowania / aktualizacji pakietów.

```PowerShell
conda create python=3.9.15 -n (nazwa_srodowiska)
conda install --file .\conda_dependencies.txt -c conda-forge -n (nazwa_srodowiska)
```

### Uruchomienie aplikacji

Znajdując się w folderze *app*:

```PowerShell
python .\start.py
```

### Tworzenie wersji EXE

Wymagane doinstalowanie pakietu *pyinstaller*:

```PowerShell
pyinstaller '.\System wyboru hoteli - Zakopane.spec'
```

Tworzy to plik wykonywalny o tej samej nazwie w folderze *dist/System wyboru hoteli - Zakopane*

W celu automatycznego pobierania listy hoteli, obok powyższego folderu należy umieścić folder *Dane* z plikiem *Hotele SWD - importowalne.xlsx*


## Informacje o kodzie

### Schemat logiki biznesowej aplikacji

Schemat przetwarzania informacji przez aplikację (bez GUI, moduł [system_wyboru_hoteli](app/system_wyboru_hoteli)):

* inicjalizacja klasy _SystemWyboruHoteli_ ([system_wyboru_hoteli.py](app/system_wyboru_hoteli/system_wyboru_hoteli.py)) i uzupełnienie o dane użytkownika,
* wykonanie wybranego rankingu:
    * sprawdzenie danych wprowadzonych przez użytkownika - zgłaszanie wyjątków ([sprawdzenie_danych_wejsciowych.py](app/system_wyboru_hoteli/sprawdzenie_danych_wejsciowych.py)),
    * wykonanie wstępnych operacji (np. filtrowania) na danych ([wstepne_przetwarzanie_kryteriow.py](app/system_wyboru_hoteli/wstepne_przetwarzanie_kryteriow.py)),
    * wykonanie rankingu wybranej metody (moduł [funkcje_rankingowe](app/system_wyboru_hoteli/funkcje_rankingowe));
* zwrócenie wyników.

Klasa _SystemWyboruHoteli_ **nie** ładuje danych z pliku, lecz otrzymuje DataFrame z danymi. Ładowanie danych jest obsługiwane przez GUI z użyciem pliku [hotel_loader.py](app/hotel_loader.py).


### Uzupełnianie metod rankingowych

W środku funkcji można tworzyć wykresy za pomocą *matplotlib.pyplot*, a następnie wyświetlać je w oknie programu po prostu wywołując *matplotlib.pyplot.show()*


### Testy jednostkowe

W folderze *test_app* znajdują się proste testy jednostkowe *pytest*, dla funkcji do uzupełnienia (oprócz jednej funkcji) - warto z tego korzystać.


