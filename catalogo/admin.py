from django.contrib import admin
from .models import Autor, ModeloLibro, ModeloEditorial, Participacion, Prestamo, Perfil
# Register your models here.
admin.site.register(Autor)

# admin.site.register(ModeloLibro)
@admin.register(ModeloLibro)
class LibroAdmin(admin.ModelAdmin):
    list_display = ("titulo", "isbn", "precio", "disponible", "editorial")
    list_filter = ("disponible", "editorial")
    search_fields = ("titulo", "isbn", "autores__nombre")
    ordering = ("titulo",)
    list_per_page = 20
admin.site.register(ModeloEditorial)
admin.site.register(Participacion)
admin.site.register(Prestamo)
admin.site.register(Perfil)