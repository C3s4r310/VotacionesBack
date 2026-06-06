from django.urls import path
from . import views

urlpatterns = [
    path('candidatos/',              views.candidatos,            name='candidatos'),
    path('votar/',                   views.votar,                 name='votar'),
    path('resultados/',              views.resultados,            name='resultados'),
    path('resultados-habilitados/',  views.resultados_habilitados, name='resultados_habilitados'),
    path('toggle-resultados/',       views.toggle_resultados,     name='toggle_resultados'),
    path('admin/votantes/',          views.admin_votantes,        name='admin_votantes'),
    path('admin/votantes/<int:pk>/', views.admin_toggle_votante,  name='admin_toggle_votante'),
]