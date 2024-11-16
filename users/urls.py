from django.urls import path
from .views import novo_usuario, alterar_senha_inicial, usuarios, listar_usuarios
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', usuarios, name='usuarios'),
    path('novo_usuario', novo_usuario, name='novo_usuario'),
    path('listar_usuarios', listar_usuarios, name='listar_usuarios'),
    path('altera_senha_inicial', alterar_senha_inicial, name='alterar_senha_inicial'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
]
