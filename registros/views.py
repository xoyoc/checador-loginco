from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from datetime import datetime, timedelta
import json
from io import BytesIO
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter

from empleados.models import Empleado
from registros.models import RegistroEmpleado

# Create your views here.


@csrf_exempt
def procesar_qr_empleado(request):
    """Procesa el escaneo de QR de empleados"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            codigo_qr = data.get('codigo_qr')
            
            # Parsear código QR
            partes = codigo_qr.split('_')
            if len(partes) >= 3 and partes[0] == 'EMP':
                empleado_id = partes[1]
                tipo_registro = partes[2]
                
                empleado = get_object_or_404(Empleado, id=empleado_id)
                
                # Registrar entrada/salida
                registro = RegistroEmpleado.objects.create(
                    empleado=empleado,
                    tipo_registro=tipo_registro,
                    codigo_qr_usado=codigo_qr
                )
                
                return JsonResponse({
                    'success': True,
                    'mensaje': f"Registro exitoso: {empleado.user.get_full_name()} - {registro.get_tipo_registro_display()}",
                    'empleado': empleado.user.get_full_name(),
                    'tipo': registro.get_tipo_registro_display(),
                    'hora': registro.fecha_hora.strftime('%H:%M:%S')
                })
            else:
                return JsonResponse({'success': False, 'error': 'Código QR inválido'})
                
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)})
    
    return render(request, 'scanner_empleado.html')


@login_required
def reporte_empleados(request):
    """Genera reporte de asistencia por período"""
    fecha_inicio = request.GET.get('fecha_inicio')
    fecha_fin = request.GET.get('fecha_fin')
    empleado_id = request.GET.get('empleado_id')
    formato = request.GET.get('formato', 'html')
    
    # Filtros por defecto (última semana)
    if not fecha_inicio:
        fecha_inicio = (timezone.now() - timedelta(days=7)).date()
    else:
        fecha_inicio = datetime.strptime(fecha_inicio, '%Y-%m-%d').date()
    
    if not fecha_fin:
        fecha_fin = timezone.now().date()
    else:
        fecha_fin = datetime.strptime(fecha_fin, '%Y-%m-%d').date()
    
    # Consulta base
    registros = RegistroEmpleado.objects.filter(
        fecha_hora__date__range=[fecha_inicio, fecha_fin]
    ).select_related('empleado__user')
    
    if empleado_id:
        registros = registros.filter(empleado_id=empleado_id)
    
    # Agrupar por empleado y fecha
    reporte_data = {}
    for registro in registros:
        empleado_nombre = registro.empleado.user.get_full_name()
        fecha = registro.fecha_hora.date()
        
        if empleado_nombre not in reporte_data:
            reporte_data[empleado_nombre] = {}
        
        if fecha not in reporte_data[empleado_nombre]:
            reporte_data[empleado_nombre][fecha] = []
        
        reporte_data[empleado_nombre][fecha].append({
            'tipo': registro.get_tipo_registro_display(),
            'hora': registro.fecha_hora.strftime('%H:%M:%S')
        })
    
    if formato == 'pdf':
        return generar_pdf_reporte(reporte_data, fecha_inicio, fecha_fin)
    
    context = {
        'reporte_data': reporte_data,
        'fecha_inicio': fecha_inicio,
        'fecha_fin': fecha_fin,
        'empleados': Empleado.objects.filter(activo=True),
        'empleado_seleccionado': empleado_id
    }
    
    return render(request, 'reporte_empleados.html', context)

def generar_pdf_reporte(reporte_data, fecha_inicio, fecha_fin):
    """Genera reporte PDF"""
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="reporte_asistencia_{fecha_inicio}_{fecha_fin}.pdf"'
    
    buffer = BytesIO()
    p = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter
    
    # Título
    p.setFont("Helvetica-Bold", 16)
    p.drawString(50, height - 50, f"Reporte de Asistencia")
    p.setFont("Helvetica", 12)
    p.drawString(50, height - 70, f"Período: {fecha_inicio} al {fecha_fin}")
    
    y_position = height - 100
    
    for empleado, fechas in reporte_data.items():
        if y_position < 100:
            p.showPage()
            y_position = height - 50
        
        p.setFont("Helvetica-Bold", 14)
        p.drawString(50, y_position, empleado)
        y_position -= 20
        
        for fecha, registros in fechas.items():
            p.setFont("Helvetica-Bold", 10)
            p.drawString(70, y_position, str(fecha))
            y_position -= 15
            
            for registro in registros:
                p.setFont("Helvetica", 9)
                p.drawString(90, y_position, f"{registro['tipo']}: {registro['hora']}")
                y_position -= 12
        
        y_position -= 10
    
    p.save()
    buffer.seek(0)
    response.write(buffer.getvalue())
    buffer.close()
    
    return response
