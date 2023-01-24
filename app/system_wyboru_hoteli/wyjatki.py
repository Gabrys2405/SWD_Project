

class BrakInicjalizacjiParametru(Exception):
    def __init__(self, nazwa_parametru: str, *args: object) -> None:
        s = f"Parametr '{nazwa_parametru}' nie został zainicjowany"
        super().__init__(s, *args)


class NiepoprawnaSzerokoscMacierzy(Exception):
    def __init__(
            self, 
            nazwa_parametru: str, 
            szerokosc_zauwazona: int, 
            szerokosc_oczekiwana: int, 
            *args: object
        ) -> None:
        s = f"Macierz w parametrze '{nazwa_parametru}' ma szerokość {szerokosc_zauwazona} (oczekiwano {szerokosc_oczekiwana})"
        super().__init__(*args)


class BladDanychUzytkownika(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)

