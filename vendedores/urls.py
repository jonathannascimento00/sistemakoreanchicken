from django.urls import path
from vendedores.views import fornecedores, novo_fornecedor, editar_fornecedor, remover_fornecedor, listar_fornecedores

urlpatterns = [
    path('', fornecedores, name='fornecedores'),
    path('novo_fornecedor', novo_fornecedor, name='novo_fornecedor'),
    path('listar_fornecedores', listar_fornecedores, name='listar_fornecedores'),
    path('editar_fornecedor/<int:pk>/', editar_fornecedor, name='editar_fornecedor'),
    path('remover_fornecedor/<int:pk>', remover_fornecedor, name='remover_fornecedor')
]