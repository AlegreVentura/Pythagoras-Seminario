# triangulo_app/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.calcular_faltante, name='calcular_faltante'),
]
