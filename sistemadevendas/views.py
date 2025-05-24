from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from pedidos.models import Produtos, Pedidos, PedidoPorProduto
from vendedores.models import Fornecedor
from estoque.models import Estoque
from django.db.models import Sum, Count, F, ExpressionWrapper, FloatField
from datetime import timedelta, date


@login_required
def home(request):
    return render(request, 'home.html')