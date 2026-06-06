from django.db import models
from usuarios.models import Votante

class Candidato(models.Model):
    nombre  = models.CharField(max_length=150)
    partido = models.CharField(max_length=150)
    foto    = models.ImageField(upload_to='candidatos/', null=True, blank=True)
    activo  = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.nombre} - {self.partido}'

class Voto(models.Model):
    votante   = models.OneToOneField(Votante, on_delete=models.CASCADE)
    candidato = models.ForeignKey(
        Candidato, on_delete=models.CASCADE,
        null=True, blank=True  # null = voto en blanco
    )
    en_blanco = models.BooleanField(default=False)
    fecha     = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        if self.en_blanco:
            return f'{self.votante.dni} — Voto en blanco'
        return f'{self.votante.dni} votó por {self.candidato.nombre}'

    class Meta:
        verbose_name        = 'Voto'
        verbose_name_plural = 'Votos'