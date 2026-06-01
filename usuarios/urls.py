from django.urls import path
from . import views

urlpatterns = [
    path('registro/',         views.registro,        name='registro'),
    path('subir-imagenes/',   views.subir_imagenes,  name='subir_imagenes'),
    path('login/',            views.login,           name='login'),
    path('perfil/',           views.perfil,          name='perfil'),
]