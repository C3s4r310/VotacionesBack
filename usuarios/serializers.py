from rest_framework import serializers
from .models import Votante

class RegistroSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=6)

    class Meta:
        model = Votante
        fields = [
            'dni', 'nombres', 'apellidos', 'fecha_nac',
            'distrito', 'departamento', 'codigo_val2', 'password'
        ]

    def create(self, validated_data):
        password = validated_data.pop('password')
        votante = Votante(**validated_data)
        votante.set_password(password)
        votante.save()
        return votante


class VotanteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Votante
        fields = [
            'id', 'dni', 'nombres', 'apellidos', 'fecha_nac',
            'distrito', 'departamento', 'validado', 'ya_voto',
            'foto_dni', 'foto_rostro', 'activo'
        ]