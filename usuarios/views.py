from rest_framework import status
from rest_framework.decorators import api_view, permission_classes, parser_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from .models import Votante
from .serializers import RegistroSerializer, VotanteSerializer

# ── Registro paso 1: datos personales ──────────────────────────────────────
@api_view(['POST'])
@permission_classes([AllowAny])
def registro(request):
    serializer = RegistroSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(
            {'mensaje': 'Votante registrado correctamente'},
            status=status.HTTP_201_CREATED
        )
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# ── Registro paso 2: subir foto DNI y rostro ───────────────────────────────
@api_view(['POST'])
@permission_classes([AllowAny])
@parser_classes([MultiPartParser, FormParser])
def subir_imagenes(request):
    dni = request.data.get('dni')
    try:
        votante = Votante.objects.get(dni=dni)
    except Votante.DoesNotExist:
        return Response({'error': 'Votante no encontrado'}, status=404)

    if 'foto_dni' in request.FILES:
        votante.foto_dni = request.FILES['foto_dni']
    if 'foto_rostro' in request.FILES:
        votante.foto_rostro = request.FILES['foto_rostro']
    votante.save()

    return Response({'mensaje': 'Imágenes guardadas correctamente'})


# ── Login ───────────────────────────────────────────────────────────────────
# @api_view(['POST'])
# @permission_classes([AllowAny])
# def login(request):
#     dni      = request.data.get('dni')
#     password = request.data.get('password')

#     votante = authenticate(request, dni=dni, password=password)
#     if not votante:
#         return Response({'error': 'DNI o contraseña incorrectos'}, status=401)

#     if not votante.activo:
#         return Response({'error': 'Tu cuenta ha sido desactivada'}, status=403)

#     refresh = RefreshToken.for_user(votante)
#     return Response({
#         'access':  str(refresh.access_token),
#         'refresh': str(refresh),
#         'votante': VotanteSerializer(votante).data
#     })
@api_view(['POST'])
@permission_classes([AllowAny])
def login(request):
    dni      = request.data.get('dni')
    password = request.data.get('password')

    votante = authenticate(request, dni=dni, password=password)
    if not votante:
        return Response({'error': 'DNI o contraseña incorrectos'}, status=401)

    if not votante.activo:
        return Response({'error': 'Tu cuenta ha sido desactivada'}, status=403)

    refresh = RefreshToken.for_user(votante)
    return Response({
        'access':   str(refresh.access_token),
        'refresh':  str(refresh),
        'is_admin': votante.is_staff,
        'votante':  VotanteSerializer(votante).data
    })


# ── Perfil del votante autenticado ─────────────────────────────────────────
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def perfil(request):
    return Response(VotanteSerializer(request.user).data)