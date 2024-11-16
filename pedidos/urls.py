from django.urls import path
from pedidos.views import novo_pedido, pedidos, listar_pedidos

urlpatterns = [
    path('', pedidos, name='pedidos'),
    path('novo_pedido', novo_pedido, name='novo_pedido'),
    path('listar_pedidos', listar_pedidos, name='listar_pedidos')
]