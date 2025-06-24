from django.contrib import admin

# Register your models here.
from .models import Visita

@admin.register(Visita)
class VisitaAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'empresa', 'persona_a_visitar', 'fecha_hora_llegada']
    list_filter = ['fecha_hora_llegada', 'empresa']
    search_fields = ['nombre', 'empresa', 'persona_a_visitar']
    date_hierarchy = 'fecha_hora_llegada'