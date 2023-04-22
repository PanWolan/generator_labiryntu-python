import pygame
import time
import random

# wymiary okna
WIDTH = 500
HEIGHT = 600
FPS = 30

# kolory dla ulatwienia pisania
WHITE = (255, 255, 255)
GREEN = (0, 255, 0,)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

# odpalanie gry
pygame.init()
pygame.mixer.init()
okno = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Generator labiryntu")
clock = pygame.time.Clock()

# zmienne potrzebne do tworzenia labiryntu
x = 0                    # pozycja x
y = 0                    # pozycja y
w = 20                   # szerokosc jednej kratki
siatka = []
odwiedzone = []
stos = []
rozwiazanie = {}


def tworzenie_siatki(x, y, w):
    for i in range(1,21):
        x = 20                                                            # startowa pozycja x
        y = y + 20                                                        # przesuwanie w dol zeby rysowac nowy rzad
        for j in range(1, 21):                                            # ramka dookola kratki
            pygame.draw.line(okno, WHITE, [x, y], [x + w, y])           # gora
            pygame.draw.line(okno, WHITE, [x + w, y], [x + w, y + w])   # prawo
            pygame.draw.line(okno, WHITE, [x + w, y + w], [x, y + w])   # dol
            pygame.draw.line(okno, WHITE, [x, y + w], [x, y])           # lewo
            siatka.append((x, y))                                            # dodaje narysowana kratke do listy siatki
            x = x + 20                                                    # przesuwanie w prawo w rzedzie zeby rysowac kolejna kratke


def gora(x, y):
    pygame.draw.rect(okno, BLUE, (x + 1, y - w + 1, 19, 39), 0)         # rysowanie prostokatu na szerokosc dwoch kratek
    pygame.display.update()                                              # tworzy wrazanie usuwania sciany a tak naprawde rysuje na niej


def dol(x, y):
    pygame.draw.rect(okno, BLUE, (x + 1, y + 1, 19, 39), 0)
    pygame.display.update()


def lewo(x, y):
    pygame.draw.rect(okno, BLUE, (x - w + 1, y + 1, 39, 19), 0)
    pygame.display.update()


def prawo(x, y):
    pygame.draw.rect(okno, BLUE, (x + 1, y + 1, 39, 19), 0)
    pygame.display.update()


def pojedyncza_kratka(x, y):
    pygame.draw.rect(okno, GREEN, (x + 1, y + 1, 18, 18), 0)          # odwiedzajac kratke koloruje ja na zielono
    pygame.display.update()


def zmiana_koloru_odwiedzonej_kratki(x, y):
    pygame.draw.rect(okno, BLUE, (x + 1, y + 1, 18, 18), 0)        # jak program odwiedza kratke to koloruja ja na zielono
    pygame.display.update()                                        # ta funkcja ostatnia odwiedzona kratke zmienia na niebieski tworzac labirynt


def rozwiazywanie_labiryntu(x,y):
    pygame.draw.rect(okno, YELLOW, (x + 8, y + 8, 5, 5), 0)             # pokazuje droga rozwiazania
    pygame.display.update()


def tworzenie_labiryntu(x, y):
    pojedyncza_kratka(x, y)                                              # poczatek tworzenia labiryntu
    stos.append((x, y))                                            # dodanie do stostu poczatkowej kratki
    odwiedzone.append((x, y))                                          # dodanie pierwszej kratki do listy odwiedzonych
    while len(stos) > 0:                                          # dopoki stos nie jest pusty
        time.sleep(.07)
        kratki = []                                                  # pomocnicza lista kratek
        if (x + w, y) not in odwiedzone and (x + w, y) in siatka:       # sprawdza czy kratka na prawo od aktualnie odwiedzonej byla juz odwiedzona
            kratki.append("prawo")                                   # jezeli jest to dodaje do listy

        if (x - w, y) not in odwiedzone and (x - w, y) in siatka:       # sprawdza czy kratka na lewo od aktualnie odwiedzonej byla juz odwiedzona
            kratki.append("lewo")

        if (x , y + w) not in odwiedzone and (x , y + w) in siatka:     # sprawdza czy kratka na dole od aktualnie odwiedzonej byla juz odwiedzona
            kratki.append("dol")

        if (x, y - w) not in odwiedzone and (x , y - w) in siatka:      # sprawdza czy kratka na gorze od aktualnie odwiedzonej byla juz odwiedzona
            kratki.append("gora")

        if len(kratki) > 0:                                          # jezeli jest jakas kratka obok obecnej jeszcze nie odwiedzona to dlugosc bedzie wieksza od 0 // max 4
            wybieranie_kratki = (random.choice(kratki))                    # wybiera losowo w ktorym kierunku z mozliwych nie odwiedzonych isc

            if wybieranie_kratki == "prawo":                             # sprawdza mozliwe przypadki losowania kolejnej kratki i wywoluje funckje rysujaca labirynt
                prawo(x, y)
                rozwiazanie[(x + w, y)] = x, y                        # solution = dictionary key = new cell, other = current cell
                x = x + w                                          #  zmienia nowo odwiedzona kratke na obecna
                odwiedzone.append((x, y))                              # dodaje do listy odwiedzonych
                stos.append((x, y))

            elif wybieranie_kratki == "lewo":
                lewo(x, y)
                rozwiazanie[(x - w, y)] = x, y
                x = x - w
                odwiedzone.append((x, y))
                stos.append((x, y))

            elif wybieranie_kratki == "dol":
                dol(x, y)
                rozwiazanie[(x , y + w)] = x, y
                y = y + w
                odwiedzone.append((x, y))
                stos.append((x, y))

            elif wybieranie_kratki == "gora":
                gora(x, y)
                rozwiazanie[(x , y - w)] = x, y
                y = y - w
                odwiedzone.append((x, y))
                stos.append((x, y))
        else:                                                            # jak nie ma juz nieodwiedzonych kratek do okola cofa sie po wczesniej odwiedzanych
            x, y = stos.pop()                                           # az spotka jakas ktora ma jakas mozliwa do odwiedzenia
            pojedyncza_kratka(x, y)
            time.sleep(.05)
            zmiana_koloru_odwiedzonej_kratki(x, y)


def droga_do_poczatku(x,y):
    rozwiazywanie_labiryntu(x, y)                                          # funkcja posiada kordy kazdego kwadratu rozwiazania
    while (x, y) != (20,20):                                     # dopoki nie wroci do poczatku
        x, y = rozwiazanie[x, y]                                    # przekazywanie do petki kolejnej kratki odwiedzonej
        rozwiazywanie_labiryntu(x, y)                                      # rysowanie drogi
        time.sleep(.1)


x, y = 20, 20                     # kordynaty lewego gornego rogu siatki
tworzenie_siatki(40, 0, 20)
tworzenie_labiryntu(x,y)
droga_do_poczatku(400, 400)


running = True
while running:
    # zmiana fps spowolni/przyspieszy
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False