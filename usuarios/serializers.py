from rest_framework import serializers
from .models import Votante

class VotanteSerializer(serializers.ModelSerializer):
    class Meta:
        model  = Votante
        fields = [
            'id', 'dni', 'nombres', 'apellidos', 'fecha_nac',
            'distrito', 'departamento', 'correo', 'foto_dni',
            'validado', 'ya_voto', 'activo'
        ]

class PadronSerializer(serializers.ModelSerializer):
    class Meta:
        model  = Votante
        fields = [
            'dni', 'nombres', 'apellidos', 'fecha_nac',
            'distrito', 'departamento', 'correo', 'foto_dni'
        ]

    def create(self, validated_data):
        password = validated_data.get('dni')
        votante  = Votante(**validated_data)
        votante.set_password(password)
        votante.save()
        return votante