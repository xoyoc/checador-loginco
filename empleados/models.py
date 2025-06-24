from django.db import models
from django.core.validators import RegexValidator
from django.contrib.auth.models import User

# Create your models here.
class Empleado(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    codigo_empleado = models.CharField(max_length=20, unique=True)
    telefono = models.CharField(max_length=15, validators=[RegexValidator(r'^\+?1?\d{9,15}$')])
    activo = models.BooleanField(default=True)
    fecha_ingreso = models.DateField()
    
    def __str__(self):
        return f"{self.user.get_full_name()} - {self.codigo_empleado}"
