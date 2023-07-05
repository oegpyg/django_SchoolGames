# from generate_fixture import generate_fixture
from datetime import date, timedelta
from core.models import Deporte, Torneo, Equipo, RondaEliminatoria, FaseEliminatoria, Encuentro
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


def run():
    _lugar = ""
    # fecha actual
    fecha_actual = date.today()
    fecha_fin = fecha_actual + timedelta(days=30)
    # Crea un objeto de modelo Deporte
    deporte = Deporte.objects.create(nombre="Fútbol")

    # Crea un objeto de modelo Torneo con la fecha de inicio actual y el deporte asociado
    # torneo = Torneo.objects.create(
    #    nombre="Mi Torneo", fecha_inicio=fecha_actual, fecha_fin=fecha_fin, deporte=deporte)
    torneo = Torneo.objects.get(nombre='Fulbol')
    # Obtener los objetos de modelo de equipos desde la base de datos
    equipos = Equipo.objects.all()

    # Crear un objeto de modelo FaseEliminatoria para el torneo
    fase_eliminatoria = FaseEliminatoria.objects.create(
        torneo=torneo, nombre="Fase Eliminatoria")

    # Generar el fixture de eliminatorias
    fixture = generate_fixture(equipos)

    # Crear las rondas y asociarlas a la fase
    for i, ronda_fixture in enumerate(fixture):
        ronda = RondaEliminatoria.objects.create(
            fase=fase_eliminatoria, nombre=f"Ronda {i+1}")
        for partido in ronda_fixture:
            equipo_local, equipo_visitante = partido
            fecha = fecha_actual
            lugar = _lugar
            nuevo_partido = Encuentro(equipo_local=equipo_local,
                                      equipo_visitante=equipo_visitante, fecha=fecha, lugar=lugar, ronda=ronda)
            nuevo_partido.save()
            # ronda.fase.objects.add(fase_eliminatoria)

    # Guardar la fase de eliminación
    fase_eliminatoria.save()
