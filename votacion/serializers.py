from rest_framework import serializers
from .models import Candidato, Voto

class CandidatoSerializer(serializers.ModelSerializer):
    class Meta:
        model  = Candidato
        fields = ['id', 'nombre', 'partido', 'foto']

class VotoSerializer(serializers.ModelSerializer):
    candidato = CandidatoSerializer(read_only=True)
    class Meta:
        model  = Voto
        fields = ['id', 'candidato', 'en_blanco', 'fecha']