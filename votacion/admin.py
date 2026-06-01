from django.contrib import admin
from .models import Candidato, Voto

admin.site.register(Candidato)
admin.site.register(Voto)