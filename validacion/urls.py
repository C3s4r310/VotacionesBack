from django.urls import path
from . import views

urlpatterns = [
    path('foto-dni/', views.validar_foto_dni, name='validar_foto_dni'),
    path('rostro/',   views.validar_rostro,   name='validar_rostro'),
]