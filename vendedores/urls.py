from django.urls import path
from . import views

urlpatterns = [
    path('vendedores/', views.vendedores, name='vendedores')
]