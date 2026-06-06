from rest_framework.decorators import api_view, permission_classes, parser_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.conf import settings
from .models import IntentoAcceso
import cv2
import numpy as np
import os
import tempfile

def comparar_rostros(ruta1, ruta2):
    """Compara dos imágenes y retorna (coincide, confianza)."""
    cascade_path = cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
    detector     = cv2.CascadeClassifier(cascade_path)

    def extraer_rostro(ruta):
        img   = cv2.imread(ruta)
        if img is None:
            return None
        gris  = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        rostros = detector.detectMultiScale(gris, scaleFactor=1.1, minNeighbors=5)
        if len(rostros) == 0:
            return None
        x, y, w, h = rostros[0]
        return cv2.resize(gris[y:y+h, x:x+w], (100, 100))

    r1 = extraer_rostro(ruta1)
    r2 = extraer_rostro(ruta2)

    if r1 is None or r2 is None:
        return False, 0.0

    diferencia = np.mean(np.abs(r1.astype(float) - r2.astype(float)))
    confianza  = round(max(0, 100 - diferencia), 2)
    coincide   = diferencia < 40

    return coincide, confianza


# ── Paso 1: Validar foto DNI subida vs foto DNI del padrón ─────────────────
@api_view(['POST'])
@permission_classes([IsAuthenticated])
@parser_classes([MultiPartParser, FormParser])
def validar_foto_dni(request):
    votante = request.user

    if not votante.foto_dni:
        return Response({'error': 'Este votante no tiene foto DNI en el padrón'}, status=400)

    if 'foto_dni' not in request.FILES:
        return Response({'error': 'Debes subir la foto de tu DNI'}, status=400)

    ruta_padron = os.path.join(settings.MEDIA_ROOT, str(votante.foto_dni))

    # Guardar foto subida temporalmente
    foto_subida = request.FILES['foto_dni']
    with tempfile.NamedTemporaryFile(delete=False, suffix='.jpg') as tmp:
        for chunk in foto_subida.chunks():
            tmp.write(chunk)
        ruta_tmp = tmp.name

    try:
        coincide, confianza = comparar_rostros(ruta_padron, ruta_tmp)
    finally:
        os.unlink(ruta_tmp)

    # Registrar intento
    IntentoAcceso.objects.create(
        votante       = votante,
        dni_ingresado = votante.dni,
        etapa         = 'foto',
        resultado     = 'exitoso' if coincide else 'fallido',
        detalle       = f'Confianza: {confianza}%'
    )

    if coincide:
        return Response({
            'validado':  True,
            'confianza': confianza,
            'mensaje':   'Foto del DNI verificada correctamente'
        })
    else:
        return Response({
            'validado':  False,
            'confianza': confianza,
            'mensaje':   'La foto del DNI no coincide con el padrón'
        }, status=400)


# ── Paso 2: Validar selfie vs foto DNI del padrón ─────────────────────────
@api_view(['POST'])
@permission_classes([IsAuthenticated])
@parser_classes([MultiPartParser, FormParser])
def validar_rostro(request):
    votante = request.user

    if not votante.foto_dni:
        return Response({'error': 'Este votante no tiene foto DNI en el padrón'}, status=400)

    if 'foto_rostro' not in request.FILES:
        return Response({'error': 'Debes capturar tu selfie'}, status=400)

    ruta_padron = os.path.join(settings.MEDIA_ROOT, str(votante.foto_dni))

    # Guardar selfie temporalmente
    selfie = request.FILES['foto_rostro']
    with tempfile.NamedTemporaryFile(delete=False, suffix='.jpg') as tmp:
        for chunk in selfie.chunks():
            tmp.write(chunk)
        ruta_tmp = tmp.name

    try:
        coincide, confianza = comparar_rostros(ruta_padron, ruta_tmp)
    finally:
        os.unlink(ruta_tmp)

    # Registrar intento
    IntentoAcceso.objects.create(
        votante       = votante,
        dni_ingresado = votante.dni,
        etapa         = 'rostro',
        resultado     = 'exitoso' if coincide else 'fallido',
        detalle       = f'Confianza: {confianza}%'
    )

    if coincide:
        votante.validado = True
        votante.save()
        return Response({
            'validado':  True,
            'confianza': confianza,
            'mensaje':   'Rostro verificado correctamente'
        })
    else:
        return Response({
            'validado':  False,
            'confianza': confianza,
            'mensaje':   'Tu rostro no coincide con la foto del DNI'
        }, status=400)