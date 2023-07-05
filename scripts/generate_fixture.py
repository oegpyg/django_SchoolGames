from random import shuffle
from itertools import combinations


def generate_fixture(equipos):
    total_equipos = len(equipos)
    rondas = total_equipos - 1
    partidos_por_ronda = total_equipos // 2

    # Generar todas las combinaciones posibles de equipos
    combinaciones = list(combinations(equipos, 2))
    shuffle(combinaciones)  # Mezclar las combinaciones aleatoriamente

    fixture = []
    for _ in range(rondas):
        ronda = []
        for j in range(partidos_por_ronda):
            partido = (combinaciones[j][0], combinaciones[j][1])
            ronda.append(partido)
        fixture.append(ronda)

        # Rotar los equipos en cada ronda, excepto el primero
        combinaciones = [combinaciones[0]] + \
            combinaciones[partidos_por_ronda:] + \
            combinaciones[1:partidos_por_ronda]

    return fixture
