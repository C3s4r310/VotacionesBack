# from rest_framework.decorators import api_view, permission_classes
# from rest_framework.permissions import IsAuthenticated, IsAdminUser
# from rest_framework.response import Response
# from rest_framework import status
# from django.db.models import Count
# from .models import Candidato, Voto
# from .serializers import CandidatoSerializer, VotoSerializer
# from usuarios.models import Votante
# from usuarios.serializers import VotanteSerializer


# # ── Listar candidatos ───────────────────────────────────────────────────────
# @api_view(['GET'])
# @permission_classes([IsAuthenticated])
# def candidatos(request):
#     lista = Candidato.objects.filter(activo=True)
#     return Response(CandidatoSerializer(lista, many=True).data)


# # ── Emitir voto ─────────────────────────────────────────────────────────────
# @api_view(['POST'])
# @permission_classes([IsAuthenticated])
# def votar(request):
#     votante = request.user

#     if not votante.validado:
#         return Response({'error': 'Debes pasar la validación facial primero'}, status=403)

#     if votante.ya_voto:
#         return Response({'error': 'Ya emitiste tu voto'}, status=403)

#     if not votante.activo:
#         return Response({'error': 'Tu cuenta está desactivada'}, status=403)

#     candidato_id = request.data.get('candidato_id')
#     if not candidato_id:
#         return Response({'error': 'Debes seleccionar un candidato'}, status=400)

#     try:
#         candidato = Candidato.objects.get(id=candidato_id, activo=True)
#     except Candidato.DoesNotExist:
#         return Response({'error': 'Candidato no válido'}, status=404)

#     Voto.objects.create(votante=votante, candidato=candidato)
#     votante.ya_voto = True
#     votante.save()

#     return Response({'mensaje': f'Voto emitido correctamente para {candidato.nombre}'})


# # ── Resultados (gráficos) ───────────────────────────────────────────────────
# @api_view(['GET'])
# @permission_classes([IsAuthenticated])
# def resultados(request):
#     datos = (
#         Voto.objects
#         .values('candidato__nombre', 'candidato__partido')
#         .annotate(total=Count('id'))
#         .order_by('-total')
#     )
#     total_votos = Voto.objects.count()

#     resultado = []
#     for d in datos:
#         resultado.append({
#             'candidato': d['candidato__nombre'],
#             'partido':   d['candidato__partido'],
#             'votos':     d['total'],
#             'porcentaje': round((d['total'] / total_votos) * 100, 2) if total_votos > 0 else 0
#         })

#     return Response({
#         'total_votos': total_votos,
#         'resultados':  resultado
#     })


# # ── Panel admin: listar votantes ────────────────────────────────────────────
# @api_view(['GET'])
# @permission_classes([IsAdminUser])
# def admin_votantes(request):
#     votantes = Votante.objects.all().order_by('-fecha_registro')
#     return Response(VotanteSerializer(votantes, many=True).data)


# # ── Panel admin: activar o desactivar votante ───────────────────────────────
# @api_view(['PATCH'])
# @permission_classes([IsAdminUser])
# def admin_toggle_votante(request, pk):
#     try:
#         votante = Votante.objects.get(pk=pk)
#     except Votante.DoesNotExist:
#         return Response({'error': 'Votante no encontrado'}, status=404)

#     votante.activo = not votante.activo
#     votante.save()

#     estado = 'activado' if votante.activo else 'desactivado'
#     return Response({'mensaje': f'Votante {estado} correctamente', 'activo': votante.activo})
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Count, Q
from .models import Candidato, Voto
from .serializers import CandidatoSerializer, VotoSerializer
from usuarios.models import Votante
from usuarios.serializers import VotanteSerializer


# ── Listar candidatos ───────────────────────────────────────────────────────
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def candidatos(request):
    lista = Candidato.objects.filter(activo=True)
    return Response(CandidatoSerializer(lista, many=True).data)


# ── Emitir voto ─────────────────────────────────────────────────────────────
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def votar(request):
    votante = request.user

    if not votante.validado:
        return Response({'error': 'Debes pasar la validación facial primero'}, status=403)
    if votante.ya_voto:
        return Response({'error': 'Ya emitiste tu voto'}, status=403)
    if not votante.activo:
        return Response({'error': 'Tu cuenta está desactivada'}, status=403)

    en_blanco    = request.data.get('en_blanco', False)
    candidato_id = request.data.get('candidato_id')

    if en_blanco:
        Voto.objects.create(votante=votante, en_blanco=True)
    else:
        if not candidato_id:
            return Response({'error': 'Debes seleccionar un candidato'}, status=400)
        try:
            candidato = Candidato.objects.get(id=candidato_id, activo=True)
        except Candidato.DoesNotExist:
            return Response({'error': 'Candidato no válido'}, status=404)
        Voto.objects.create(votante=votante, candidato=candidato)

    votante.ya_voto = True
    votante.save()

    return Response({'mensaje': 'Voto emitido correctamente'})


# ── Resultados y métricas (solo admin) ─────────────────────────────────────
@api_view(['GET'])
@permission_classes([IsAdminUser])
def resultados(request):
    total_registrados = Votante.objects.filter(activo=True).count()
    total_votos       = Voto.objects.count()
    votos_blanco      = Voto.objects.filter(en_blanco=True).count()
    ausentes          = total_registrados - total_votos
    participacion     = round((total_votos / total_registrados) * 100, 2) if total_registrados > 0 else 0

    # Votos por candidato
    por_candidato = (
        Voto.objects
        .filter(en_blanco=False)
        .values('candidato__nombre', 'candidato__partido')
        .annotate(total=Count('id'))
        .order_by('-total')
    )

    resultados_lista = []
    for d in por_candidato:
        resultados_lista.append({
            'candidato':  d['candidato__nombre'],
            'partido':    d['candidato__partido'],
            'votos':      d['total'],
            'porcentaje': round((d['total'] / total_votos) * 100, 2) if total_votos > 0 else 0,
        })

    # Agregar voto en blanco a la lista
    if votos_blanco > 0:
        resultados_lista.append({
            'candidato':  'Voto en Blanco',
            'partido':    '—',
            'votos':      votos_blanco,
            'porcentaje': round((votos_blanco / total_votos) * 100, 2) if total_votos > 0 else 0,
        })

    # Votos por departamento
    por_departamento = (
        Voto.objects
        .values('votante__departamento')
        .annotate(total=Count('id'))
        .order_by('-total')
    )

    # Votos por distrito
    por_distrito = (
        Voto.objects
        .values('votante__distrito', 'votante__departamento')
        .annotate(total=Count('id'))
        .order_by('-total')
    )

    return Response({
        'resumen': {
            'total_registrados': total_registrados,
            'total_votos':       total_votos,
            'votos_blanco':      votos_blanco,
            'ausentes':          ausentes,
            'participacion':     participacion,
        },
        'por_candidato':    resultados_lista,
        'por_departamento': [
            {
                'departamento': d['votante__departamento'],
                'votos':        d['total'],
                'porcentaje':   round((d['total'] / total_votos) * 100, 2) if total_votos > 0 else 0,
            }
            for d in por_departamento
        ],
        'por_distrito': [
            {
                'distrito':     d['votante__distrito'],
                'departamento': d['votante__departamento'],
                'votos':        d['total'],
            }
            for d in por_distrito
        ],
    })


# ── Panel admin: listar votantes ────────────────────────────────────────────
@api_view(['GET'])
@permission_classes([IsAdminUser])
def admin_votantes(request):
    votantes = Votante.objects.all().order_by('-fecha_registro')
    return Response(VotanteSerializer(votantes, many=True).data)


# ── Panel admin: activar o desactivar votante ───────────────────────────────
@api_view(['PATCH'])
@permission_classes([IsAdminUser])
def admin_toggle_votante(request, pk):
    try:
        votante = Votante.objects.get(pk=pk)
    except Votante.DoesNotExist:
        return Response({'error': 'Votante no encontrado'}, status=404)

    votante.activo = not votante.activo
    votante.save()
    estado = 'activado' if votante.activo else 'desactivado'
    return Response({'mensaje': f'Votante {estado} correctamente', 'activo': votante.activo})


# ── Admin: activar/desactivar resultados públicos ───────────────────────────
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def resultados_habilitados(request):
    # Retorna si los resultados están habilitados
    from django.core.cache import cache
    habilitado = cache.get('resultados_habilitados', False)
    return Response({'habilitado': habilitado})


@api_view(['POST'])
@permission_classes([IsAdminUser])
def toggle_resultados(request):
    from django.core.cache import cache
    actual     = cache.get('resultados_habilitados', False)
    nuevo      = not actual
    cache.set('resultados_habilitados', nuevo, timeout=None)
    return Response({'habilitado': nuevo, 'mensaje': f"Resultados {'habilitados' if nuevo else 'deshabilitados'}"})