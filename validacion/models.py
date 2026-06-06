from django.db import models
from usuarios.models import Votante

class IntentoAcceso(models.Model):
    RESULTADO_CHOICES = [
        ('exitoso', 'Exitoso'),
        ('fallido', 'Fallido'),
    ]
    ETAPA_CHOICES = [
        ('dni',    'Verificación DNI'),
        ('foto',   'Foto DNI'),
        ('rostro', 'Rostro'),
    ]

    votante   = models.ForeignKey(Votante, on_delete=models.CASCADE, null=True, blank=True)
    dni_ingresado = models.CharField(max_length=8)
    etapa     = models.CharField(max_length=20, choices=ETAPA_CHOICES)
    resultado = models.CharField(max_length=20, choices=RESULTADO_CHOICES)
    fecha     = models.DateTimeField(auto_now_add=True)
    detalle   = models.TextField(blank=True)

    def __str__(self):
        return f'{self.dni_ingresado} - {self.etapa} - {self.resultado}'

    class Meta:
        verbose_name        = 'Intento de Acceso'
        verbose_name_plural = 'Intentos de Acceso'