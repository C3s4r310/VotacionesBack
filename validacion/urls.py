from django.urls import path
from . import views

urlpatterns = [
    path('rostro/', views.validar_rostro, name='validar_rostro'),
]