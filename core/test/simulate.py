from generate_fixture import generate_fixture
from datetime import date
from core.models import Deporte, Torneo, Equipo, RondaEliminatoria, FaseEliminatoria, Partido

_lugar = ""
# fecha actual
fecha_actual = date.today()

# Crea un objeto de modelo Deporte
deporte = Deporte.objects.create(nombre="Fútbol")

# Crea un objeto de modelo Torneo con la fecha de inicio actual y el deporte asociado
torneo = Torneo.objects.create(
    nombre="Mi Torneo", fecha_inicio=fecha_actual, deporte=deporte)

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
        nuevo_partido = Partido(torneo=torneo, equipo_local=equipo_local,
                                equipo_visitante=equipo_visitante, fecha=fecha, lugar=lugar)
        nuevo_partido.save()
        ronda.partidos.add(nuevo_partido)

# Guardar la fase de eliminación
fase_eliminatoria.save()
