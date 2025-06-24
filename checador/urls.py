"""
URL configuration for checador project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from empleados.views import *
from registros.views import *
from visitas.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', dashboard_empleados, name='dashboard'),
    path('qr/empleado/', generar_qr_empleado, name='generar_qr_empleado'),
    path('qr/visita/', generar_qr_visita, name='generar_qr_visita'),
    path('scanner/empleado/', procesar_qr_empleado, name='scanner_empleado'),
    path('visita/formulario/', formulario_visita, name='formulario_visita'),
    path('visita/confirmacion/<int:visita_id>/', confirmacion_visita, name='confirmacion_visita'),
    path('reporte/', reporte_empleados, name='reporte_empleados'),
]