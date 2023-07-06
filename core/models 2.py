from django.db import models
from django.contrib import admin


class Torneo(models.Model):
    """Donde se carga la olimpiada corriente"""
    nombre = models.CharField(max_length=100)
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()

    def __str__(self):
        return self.nombre


class Deporte(models.Model):
    """Ejemplo: Futbol masculino, Futbol Femenino, Canto Masculino Solista"""
    codigo = models.CharField(max_length=5, help_text="Codigo Corto", default="")
    nombre = models.CharField(max_length=100, help_text="Descripcion")
    torneo = models.ForeignKey(Torneo, on_delete=models.CASCADE)

    def __str__(self):
        return self.nombre


class Color(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    puntos = models.IntegerField(default=0)
    torneo = models.ForeignKey(Torneo, on_delete=models.CASCADE)
    def __str__(self):
        return self.nombre

    def aumentar_puntos(self, cantidad):
        self.puntos += cantidad
        self.save()

    class Admin(admin.ModelAdmin):
        list_filter = ['torneo']
        list_display = ['id', 'nombre', 'puntos', 'torneo']


class Equipo(models.Model):
    nombre = models.CharField(max_length=100)
    torneo = models.ForeignKey(
        Torneo, on_delete=models.CASCADE, related_name='equipos')
    color = models.ForeignKey(
        Color, on_delete=models.CASCADE, related_name='colores')
    puntos = models.IntegerField(default=0)

    def __str__(self):
        return f'[{self.color}] {self.nombre} '

    def aumentar_puntos(self, cantidad):
        self.puntos += cantidad
        self.save()


class Jugador(models.Model):
    nombre = models.CharField(max_length=100)
    equipo = models.ForeignKey(
        Equipo, on_delete=models.CASCADE, related_name='jugadores', null=True, blank=True)
    color = models.ForeignKey(
        Color, on_delete=models.CASCADE, related_name='color_jugador')
    def __str__(self):
        return self.nombre

    class Admin(admin.ModelAdmin):
        list_display = ['id', 'nombre', 'equipo', 'color']

class ColorDeportePuntos(models.Model):
    torneo = models.ForeignKey(Torneo, on_delete=models.CASCADE)
    color = models.ForeignKey(Color, on_delete=models.CASCADE, related_name="color")
    deporte = models.ForeignKey(Deporte, on_delete=models.CASCADE)
    puntos = models.IntegerField(default=0)

    def __str__(self):
        return f'[{self.color}] {self.deporte}: {self.puntos} '

    class Admin(admin.ModelAdmin):
        list_display = ['torneo', 'color', 'deporte', 'puntos']


class Encuentro(models.Model):
    torneo = models.ForeignKey(Torneo, on_delete=models.CASCADE)
    deporte = models.ForeignKey(Deporte, on_delete=models.CASCADE)
    #puede equipo contra equipo
    equipo_local = models.ForeignKey(
        Equipo, on_delete=models.CASCADE, related_name='encuentros_locales', null=True, blank=True)
    equipo_visitante = models.ForeignKey(
        Equipo, on_delete=models.CASCADE, related_name='encuentros_visitantes', null=True, blank=True)
    #puede ser solo de jugadores
    jugador_local = models.ForeignKey(
        Jugador, on_delete=models.CASCADE, related_name='encuentros_locales', null=True, blank=True)
    judador_visitante = models.ForeignKey(
        Jugador, on_delete=models.CASCADE, related_name='encuentros_visitantes', null=True, blank=True)

    fecha = models.DateTimeField(blank=True, null=True)
    lugar = models.CharField(max_length=100, blank=True)
    resultado_local = models.PositiveIntegerField(blank=True, null=True)
    resultado_visitante = models.PositiveIntegerField(blank=True, null=True)
    #equipo o jugador ganador
    equipo_ganador = models.ForeignKey(Equipo, on_delete=models.CASCADE, blank=True, null=True,
                                       related_name='encuentros_e_ganados')
    jugador_ganador = models.ForeignKey(Jugador, on_delete=models.CASCADE, blank=True, null=True,
                                       related_name='encuentros_j_ganados')

    puntos_ganador = models.IntegerField(
        default=3, help_text="Define los puntos otorgados al ganador")
    puntos_empate = models.IntegerField(
        default=1, help_text="Define los puntos otorgados el empate")
    finalizado = models.BooleanField(default=False)

    def __str__(self):
        if self.equipo_local and self.equipo_visitante:
            return f"{self.equipo_local} vs {self.equipo_visitante}"
        else:
            return f"{self.jugador_local} vs {self.judador_visitante}"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.finalizado:
            # Realizar el acumulado de puntos cuanto el encuentro finalice
            es_equipo = True if self.equipo_visitante and self.equipo_local else False
            if self.resultado_local > self.resultado_visitante:
                if es_equipo:
                    # Sumar puntos al equipo local
                    self.equipo_local.aumentar_puntos(self.puntos_ganador)
                    self.equipo_local.color.aumentar_puntos(self.puntos_ganador)
                    self.equipo_ganador = self.equipo_local
                else:
                    self.jugador_local.color.aumentar_puntos(self.puntos_ganador)
                    self.jugador_ganador = self.jugador_local
                tmpcolorL = self.equipo_local.color if es_equipo else self.jugador_local.color
                depcolp = ColorDeportePuntos.objects.get_or_create(torneo=self.torneo,
                                                                   color=tmpcolorL,
                                                                   deporte=self.deporte)
                depcolp[0].puntos += self.puntos_ganador
                depcolp[0].save()
            elif self.resultado_local < self.resultado_visitante:
                if es_equipo:
                    # Sumar puntos al equipo visitante
                    self.equipo_visitante.aumentar_puntos(self.puntos_ganador)
                    self.equipo_visitante.color.aumentar_puntos(self.puntos_ganador)
                    self.equipo_ganador = self.equipo_visitante
                else:
                    self.jugador_visitante.color.aumentar_puntos(self.puntos_ganador)
                    self.jugador_ganador = self.jugador_visitante
                tmpcolorV = self.equipo_visitante.color if es_equipo else self.jugador_visitante.color
                depcolp = ColorDeportePuntos.objects.get_or_create(torneo=self.torneo,
                                                                   color=tmpcolorV,
                                                                   deporte=self.deporte)
                depcolp[0].puntos += self.puntos_ganador
                depcolp[0].save()
            else:
                if es_equipo:
                    # Sumar punto a cada equipo por empate
                    self.equipo_local.aumentar_puntos(self.puntos_empate)
                    self.equipo_local.color.aumentar_puntos(self.puntos_empate)
                    self.equipo_visitante.aumentar_puntos(self.puntos_empate)
                    self.equipo_visitante.color.aumentar_puntos(self.puntos_empate)
                else:
                    self.jugador_local.color.aumentar_puntos(self.puntos_empate)
                    self.jugador_visitante.color.aumentar_puntos(self.puntos_empate)

                tmpcolorL = self.equipo_local.color if es_equipo else self.jugador_local.color
                depcolp = ColorDeportePuntos.objects.get_or_create(torneo=self.torneo,
                                                                   color=tmpcolorL,
                                                                   deporte=self.deporte)
                depcolp[0].puntos += self.puntos_empate
                depcolp[0].save()

                tmpcolorV = self.equipo_local.color if es_equipo else self.jugador_local.color
                depcolp2 = ColorDeportePuntos.objects.get_or_create(torneo=self.torneo,
                                                                    color=tmpcolorV,
                                                                    deporte=self.deporte)
                depcolp2[0].puntos += self.puntos_empate
                depcolp2[0].save()

    class Admin(admin.ModelAdmin):
        list_display = ['id', 'equipo_ganador', 'jugador_ganador', 'resultado_local', 'resultado_visitante', 'finalizado']
