from django.urls import path
from . import views

urlpatterns = [
    path('verificar-dni/',          views.verificar_dni,         name='verificar_dni'),
    path('subir-rostro/',           views.subir_rostro,          name='subir_rostro'),
    path('perfil/',                 views.perfil,                name='perfil'),
    path('admin/crear/',            views.admin_crear_votante,   name='admin_crear_votante'),
    path('admin/editar/<int:pk>/',  views.admin_editar_votante,  name='admin_editar_votante'),
    path('admin/eliminar/<int:pk>/',views.admin_eliminar_votante,name='admin_eliminar_votante'),
    path('login/', views.login, name='login'),
]