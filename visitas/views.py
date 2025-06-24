from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db.models import Q
from django.utils import timezone
import qrcode
from io import BytesIO
import base64

from visitas.models import Visita

# Create your views here.
def generar_qr_visita(request):
    """Genera código QR para registro de visitas"""
    timestamp = timezone.now().strftime('%Y%m%d%H%M%S')
    codigo = f"VISITA_REGISTRO_{timestamp}"
    
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

def formulario_visita(request):
    """Formulario para registro de visitas"""
    if request.method == 'POST':
        try:
            visita = Visita.objects.create(
                nombre=request.POST.get('nombre'),
                empresa=request.POST.get('empresa', ''),
                email=request.POST.get('email'),
                telefono=request.POST.get('telefono'),
                persona_a_visitar=request.POST.get('persona_a_visitar'),
                motivo_visita=request.POST.get('motivo_visita'),
                codigo_qr_usado=request.POST.get('codigo_qr', '')
            )
            
            messages.success(request, 'Visita registrada exitosamente')
            return redirect('confirmacion_visita', visita_id=visita.id)
            
        except Exception as e:
            messages.error(request, f'Error al registrar visita: {str(e)}')
    
    return render(request, 'formulario_visita.html')

def confirmacion_visita(request, visita_id):
    """Confirmación de registro de visita"""
    visita = get_object_or_404(Visita, id=visita_id)
    return render(request, 'confirmacion_visita.html', {'visita': visita})
