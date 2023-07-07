from django.contrib import admin
from django.apps import apps
from .models import Jugador, Equipo
# Nombre de la aplicación que deseas registrar en el administrador
nombre_aplicacion = 'core'

# Obtiene todos los modelos registrados en la aplicación especificada
modelos = apps.get_app_config(nombre_aplicacion).get_models()

# Registra todos los modelos en el administrador
for modelo in modelos:
    if 'Admin' in modelo.__dict__:
        admin.site.register(modelo, modelo.Admin)
    else:
        if 'no_admin' in modelo.__dict__:
            pass
        else:
            admin.site.register(modelo)


#Custom Admins
class JugadorEquipoAdmin(admin.TabularInline):
    model = Jugador
    extra = 1


class EquipoAdmin(admin.ModelAdmin):
   fields = ('nombre', 'torneo', 'color', 'puntos')
   inlines = [JugadorEquipoAdmin, ]


admin.site.register(Equipo, EquipoAdmin)
