from django.db import models
from django.utils import timezone

# Create your models here.
class Visita(models.Model):
    nombre = models.CharField(max_length=100)
    empresa = models.CharField(max_length=100, blank=True)
    email = models.EmailField()
    telefono = models.CharField(max_length=15)
    persona_a_visitar = models.CharField(max_length=100)
    motivo_visita = models.TextField()
    fecha_hora_llegada = models.DateTimeField(default=timezone.now)
    fecha_hora_salida = models.DateTimeField(null=True, blank=True)
    codigo_qr_usado = models.CharField(max_length=100)
    
    def __str__(self):
        return f"{self.nombre} - {self.empresa} - {self.fecha_hora_llegada}"