from rest_framework import status
from rest_framework.decorators import api_view, permission_classes, parser_classes
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from .models import Votante
from .serializers import VotanteSerializer, PadronSerializer


# ── Verificar DNI (paso 1) ──────────────────────────────────────────────────
@api_view(['POST'])
@permission_classes([AllowAny])
def verificar_dni(request):
    dni = request.data.get('dni', '').strip()

    if not dni or len(dni) != 8:
        return Response({'error': 'DNI inválido'}, status=400)

    try:
        votante = Votante.objects.get(dni=dni, activo=True)
    except Votante.DoesNotExist:
        return Response({'error': 'DNI no encontrado en el padrón electoral'}, status=404)

    if votante.ya_voto:
        return Response({'error': 'Este DNI ya emitió su voto'}, status=403)

    if not votante.foto_dni:
        return Response({'error': 'Este votante no tiene foto DNI registrada'}, status=400)

    # Generar token temporal para continuar el flujo
    refresh = RefreshToken.for_user(votante)
    return Response({
        'mensaje': 'DNI verificado correctamente',
        'access':  str(refresh.access_token),
        'votante': {
            'dni':      votante.dni,
            'nombres':  votante.nombres,
            'apellidos': votante.apellidos,
        }
    })


# ── Subir foto rostro (paso 2) ──────────────────────────────────────────────
@api_view(['POST'])
@permission_classes([IsAuthenticated])
@parser_classes([MultiPartParser, FormParser])
def subir_rostro(request):
    votante = request.user

    if 'foto_rostro' not in request.FILES:
        return Response({'error': 'Debes subir una foto de tu rostro'}, status=400)

    votante.foto_rostro = request.FILES['foto_rostro']
    votante.save()

    return Response({'mensaje': 'Foto de rostro guardada correctamente'})


# ── Perfil del votante autenticado ─────────────────────────────────────────
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def perfil(request):
    return Response(VotanteSerializer(request.user).data)


# ── Admin: cargar votante al padrón ────────────────────────────────────────
@api_view(['POST'])
@permission_classes([IsAdminUser])
@parser_classes([MultiPartParser, FormParser])
def admin_crear_votante(request):
    serializer = PadronSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({'mensaje': 'Votante agregado al padrón'}, status=201)
    return Response(serializer.errors, status=400)


# ── Admin: editar votante ──────────────────────────────────────────────────
@api_view(['PUT', 'PATCH'])
@permission_classes([IsAdminUser])
@parser_classes([MultiPartParser, FormParser])
def admin_editar_votante(request, pk):
    try:
        votante = Votante.objects.get(pk=pk)
    except Votante.DoesNotExist:
        return Response({'error': 'Votante no encontrado'}, status=404)

    serializer = PadronSerializer(votante, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response({'mensaje': 'Votante actualizado correctamente'})
    return Response(serializer.errors, status=400)


# ── Admin: eliminar votante ────────────────────────────────────────────────
@api_view(['DELETE'])
@permission_classes([IsAdminUser])
def admin_eliminar_votante(request, pk):
    try:
        votante = Votante.objects.get(pk=pk)
    except Votante.DoesNotExist:
        return Response({'error': 'Votante no encontrado'}, status=404)
    votante.delete()
    return Response({'mensaje': 'Votante eliminado del padrón'})