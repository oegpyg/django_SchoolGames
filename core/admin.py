from django.contrib import admin
from django.apps import apps

# Nombre de la aplicación que deseas registrar en el administrador
nombre_aplicacion = 'core'

# Obtiene todos los modelos registrados en la aplicación especificada
modelos = apps.get_app_config(nombre_aplicacion).get_models()

# Registra todos los modelos en el administrador
for modelo in modelos:
    if 'Admin' in modelo.__dict__:
        admin.site.register(modelo, modelo.Admin)
    else:
        admin.site.register(modelo)
