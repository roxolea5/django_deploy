from django.contrib import admin

# Register your models here.
from .models import User, Zona, Tour, Salida

class UserAdmin(admin.ModelAdmin):
    # Se sobre escribe lo que hace __str__
    list_display = ("id", "nombre", "apellidos", "email", "fechaNacimiento",
        "genero", "tipo")

class TourAdmin(admin.ModelAdmin):
    # Se sobre escribe lo que hace __str__
    list_display = ("id", "nombre", "slug", "operador", "tipoDeTour",
        "descripcion", "pais", "zonaSalida", "zonaLlegada")

class SalidaAdmin(admin.ModelAdmin):
    # Se sobre escribe lo que hace __str__
    list_display = ("id", "fechaInicio", "fechaFin", "asientos", "precio",
        "tour")

admin.site.register(User, UserAdmin)
admin.site.register(Zona)
admin.site.register(Tour, TourAdmin)
admin.site.register(Salida, SalidaAdmin)
