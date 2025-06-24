from django.contrib import admin

# Register your models here.
from .models import Empleado

@admin.register(Empleado)
class EmpleadoAdmin(admin.ModelAdmin):
    list_display = ['user', 'codigo_empleado', 'telefono', 'activo', 'fecha_ingreso']
    list_filter = ['activo', 'fecha_ingreso']
    search_fields = ['user__first_name', 'user__last_name', 'codigo_empleado']