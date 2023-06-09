from django.db import models


class Deporte(models.Model):
    nombre = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre


class Torneo(models.Model):
    nombre = models.CharField(max_length=100)
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()
    deporte = models.ForeignKey(Deporte, on_delete=models.CASCADE)

    def __str__(self):
        return self.nombre


class Color(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    puntos = models.IntegerField(default=0)

    def __str__(self):
        return self.nombre

    def aumentar_puntos(self, cantidad):
        self.puntos += cantidad
        self.save()


class Equipo(models.Model):
    nombre = models.CharField(max_length=100)
    torneo = models.ForeignKey(
        Torneo, on_delete=models.CASCADE, related_name='equipos')
    color = models.ForeignKey(
        Color, on_delete=models.CASCADE, related_name='colores')
    puntos = models.IntegerField(default=0)

    def __str__(self):
        return self.nombre

    def aumentar_puntos(self, cantidad):
        self.puntos += cantidad
        self.save()


class Jugador(models.Model):
    nombre = models.CharField(max_length=100)
    equipo = models.ForeignKey(
        Equipo, on_delete=models.CASCADE, related_name='jugadores')

    def __str__(self):
        return self.nombre


"""
FaseEliminatoria, RondaEliminatoria y Encuentro para manejar las eliminatorias del torneo. 
La clase FaseEliminatoria representa una fase específica de eliminación directa dentro del torneo. 
La clase RondaEliminatoria representa una ronda dentro de una fase eliminatoria, 
como "Octavos de final", "Cuartos de final", etc.
La clase Encuentro representa un enfrentamiento específico entre dos equipos en una ronda de eliminación.

La clase FaseEliminatoria tiene una relación uno a uno (OneToOneField) con la clase Torneo, 
mientras que la clase RondaEliminatoria tiene una relación de muchos a uno (ForeignKey)
"""


class FaseEliminatoria(models.Model):
    torneo = models.OneToOneField(
        Torneo, on_delete=models.CASCADE, related_name='fase_eliminacion')
    nombre = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre


class RondaEliminatoria(models.Model):
    fase = models.ForeignKey(
        FaseEliminatoria, on_delete=models.CASCADE, related_name='rondas')
    nombre = models.CharField(max_length=100)

    def __str__(self):
        return self.nombre


class Encuentro(models.Model):
    ronda = models.ForeignKey(
        RondaEliminatoria, on_delete=models.CASCADE, related_name='encuentros')
    equipo_local = models.ForeignKey(
        Equipo, on_delete=models.CASCADE, related_name='encuentros_locales')
    equipo_visitante = models.ForeignKey(
        Equipo, on_delete=models.CASCADE, related_name='encuentros_visitantes')
    fecha = models.DateTimeField(blank=True, null=True)
    lugar = models.CharField(max_length=100, blank=True)
    resultado_local = models.PositiveIntegerField(blank=True, null=True)
    resultado_visitante = models.PositiveIntegerField(blank=True, null=True)
    ganador = models.ForeignKey(Equipo, on_delete=models.CASCADE,
                                blank=True, null=True, related_name='encuentros_ganados')
    puntos_ganador = models.IntegerField(
        default=3, help_text="Define los puntos otorgados al ganador")
    puntos_empate = models.IntegerField(
        default=1, help_text="Define los puntos otorgados al ganador")
    finalizado = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.equipo_local} vs {self.equipo_visitante}"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.finalizado:
            # Realizar el calculo de puntos cuanto el encuentro finalice
            if self.resultado_local > self.resultado_visitante:
                # Sumar puntos al equipo local
                self.equipo_local.aumentar_puntos(self.puntos_ganador)
                self.equipo_local.color.aumentar_puntos(self.puntos_ganador)
            elif self.resultado_local < self.resultado_visitante:
                # Sumar puntos al equipo visitante
                self.equipo_visitante.aumentar_puntos(self.puntos_ganador)
                self.equipo_visitante.color.aumentar_puntos(
                    self.puntos_ganador)
            else:
                # Sumar punto a cada equipo por empate
                self.equipo_local.aumentar_puntos(self.puntos_empate)
                self.equipo_local.color.aumentar_puntos(self.puntos_empate)
                self.equipo_visitante.aumentar_puntos(self.puntos_empate)
                self.equipo_visitante.color.aumentar_puntos(self.puntos_empate)
