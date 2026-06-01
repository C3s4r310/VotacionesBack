from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.conf import settings
import cv2
import numpy as np
import os

def detectar_rostro(ruta):
    """Detecta y extrae el rostro de una imagen."""
    cascade_path = cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
    detector     = cv2.CascadeClassifier(cascade_path)
    img          = cv2.imread(ruta)
    gris         = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    rostros      = detector.detectMultiScale(gris, scaleFactor=1.1, minNeighbors=5)
    if len(rostros) == 0:
        return None
    x, y, w, h = rostros[0]
    return cv2.resize(gris[y:y+h, x:x+w], (100, 100))


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def validar_rostro(request):
    votante = request.user

    if not votante.foto_dni or not votante.foto_rostro:
        return Response({'error': 'No tienes imágenes registradas'}, status=400)

    ruta_dni    = os.path.join(settings.MEDIA_ROOT, str(votante.foto_dni))
    ruta_rostro = os.path.join(settings.MEDIA_ROOT, str(votante.foto_rostro))

    try:
        rostro_dni    = detectar_rostro(ruta_dni)
        rostro_selfie = detectar_rostro(ruta_rostro)

        if rostro_dni is None:
            return Response({'error': 'No se detectó rostro en la foto del DNI'}, status=400)
        if rostro_selfie is None:
            return Response({'error': 'No se detectó rostro en la selfie'}, status=400)

        # Comparar usando diferencia de píxeles normalizada
        diferencia = np.mean(np.abs(rostro_dni.astype(float) - rostro_selfie.astype(float)))
        confianza  = round(max(0, 100 - diferencia), 2)
        es_valido  = diferencia < 40  # umbral ajustable

        if es_valido:
            votante.validado = True
            votante.save()

        return Response({
            'validado':  es_valido,
            'confianza': confianza,
            'mensaje':   'Rostro validado correctamente' if es_valido else 'El rostro no coincide con la foto del DNI'
        })

    except Exception as e:
        return Response({'error': f'Error al procesar imágenes: {str(e)}'}, status=500)