from django.contrib import admin

# Register your models here.
from .models import RegistroEmpleado

@admin.register(RegistroEmpleado)
class RegistroEmpleadoAdmin(admin.ModelAdmin):
    list_display = ['empleado', 'tipo_registro', 'fecha_hora']
    list_filter = ['tipo_registro', 'fecha_hora']
    search_fields = ['empleado__user__first_name', 'empleado__user__last_name']
    date_hierarchy = 'fecha_hora'