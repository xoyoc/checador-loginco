from django.db import models
from django.utils import timezone

from empleados.models import Empleado

# Create your models here.
class TipoRegistro(models.TextChoices):
    ENTRADA = 'entrada', 'Entrada'
    SALIDA = 'salida', 'Salida'
    COMIDA_SALIDA = 'comida_salida', 'Salida a Comida'
    COMIDA_ENTRADA = 'comida_entrada', 'Regreso de Comida'

class RegistroEmpleado(models.Model):
    empleado = models.ForeignKey(Empleado, on_delete=models.CASCADE)
    tipo_registro = models.CharField(max_length=20, choices=TipoRegistro.choices)
    fecha_hora = models.DateTimeField(default=timezone.now)
    codigo_qr_usado = models.CharField(max_length=100)
    
    class Meta:
        ordering = ['-fecha_hora']
    
    def __str__(self):
        return f"{self.empleado} - {self.get_tipo_registro_display()} - {self.fecha_hora}"
