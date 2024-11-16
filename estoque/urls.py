from django.urls import path
from estoque.views import estoque, listar_estoque, cadastrar_estoque, remover_produto, editar_produto

urlpatterns = [
    path('', estoque, name='estoque'),
    path('listar_estoque', listar_estoque, name='listar_estoque'),
    path('cadastrar_estoque', cadastrar_estoque, name='cadastrar_estoque'),
    path('editar_produto/<int:produto>/', editar_produto, name='editar_produto'),
    path('remover_produto/<int:produto>', remover_produto, name='remover_produto')
]