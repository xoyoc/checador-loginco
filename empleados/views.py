from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.utils import timezone
import qrcode
from io import BytesIO
import base64

# Create your views here.
from .models import Empleado
from registros.models import RegistroEmpleado

@login_required
def dashboard_empleados(request):
    """Dashboard con registros de empleados"""
    fecha_hoy = timezone.now().date()
    
    # Registros del día
    registros_hoy = RegistroEmpleado.objects.filter(
        fecha_hora__date=fecha_hoy
    ).select_related('empleado__user')
    
    # Empleados presentes (última entrada sin salida)
    empleados_presentes = []
    for empleado in Empleado.objects.filter(activo=True):
        ultimo_registro = RegistroEmpleado.objects.filter(
            empleado=empleado,
            fecha_hora__date=fecha_hoy
        ).first()
        
        if ultimo_registro and ultimo_registro.tipo_registro in ['entrada', 'comida_entrada']:
            empleados_presentes.append(empleado)
    
    context = {
        'registros_hoy': registros_hoy,
        'empleados_presentes': empleados_presentes,
        'total_registros': registros_hoy.count(),
        'fecha_hoy': fecha_hoy
    }
    
    return render(request, 'dashboard.html', context)


def generar_qr_empleado(request):
    """Genera códigos QR únicos para empleados"""
    if request.method == 'POST':
        empleado_id = request.POST.get('empleado_id')
        tipo = request.POST.get('tipo', 'entrada')
        
        # Generar código único
        timestamp = timezone.now().strftime('%Y%m%d%H%M%S')
        codigo = f"EMP_{empleado_id}_{tipo}_{timestamp}"
        
        # Crear QR
        qr = qrcode.QRCode(version=1, box_size=10, border=5)
        qr.add_data(codigo)
        qr.make(fit=True)
        
        img = qr.make_image(fill_color="black", back_color="white")
        buffer = BytesIO()
        img.save(buffer, format='PNG')
        img_str = base64.b64encode(buffer.getvalue()).decode()
        
        return JsonResponse({
            'qr_code': f"data:image/png;base64,{img_str}",
            'codigo': codigo
        })
    
    empleados = Empleado.objects.filter(activo=True)
    return render(request, 'generar_qr.html', {'empleados': empleados})
