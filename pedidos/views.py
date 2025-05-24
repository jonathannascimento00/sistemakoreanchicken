from decimal import Decimal
from django.shortcuts import render
from django.template import loader, RequestContext
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from vendedores.models import Fornecedor
from .models import Produtos, Pedidos, PedidoPorProduto
from django.contrib.auth.decorators import login_required
from django.db.models import Sum, Count, F
from datetime import datetime, timedelta
from django.utils.timezone import now
import json

@login_required
def pedidos(request):
    return render(request, 'pedidos/index.html')

@login_required
def listar_pedidos(request):
    pedidos = Pedidos.objects.all()
    return render(request, 'pedidos/listar_pedidos.html', {'pedidos' : pedidos})

@login_required
def novo_pedido(request):
    if request.method == 'POST':
        fornecedor_id = request.POST.get('fornecedor')
        fornecedor = Fornecedor.objects.get(id=fornecedor_id)

        # Criação do Pedido
        pedido = Pedidos.objects.create(fornecedor=fornecedor)

        # Captura os dados dos produtos (id, quantidade e valor_unitario) enviados pelo formulário
        produtos_ids = request.POST.getlist('produtos[][produto]')
        produtos_quantidade = request.POST.getlist('produtos[][quantidade]')
        produtos_valor_unitario = request.POST.getlist('produtos[][valor_unitario]')

        # Inicializa o valor total do pedido
        valor_total = 0

        # Para cada produto, cria uma entrada na tabela PedidoPorProduto
        for produto_id, quantidade, valor_unitario in zip(produtos_ids, produtos_quantidade, produtos_valor_unitario):
            # Obtém o produto correspondente ao id
            produto = Produtos.objects.get(id_produto=produto_id)
            
            # Cria a entrada na tabela PedidoPorProduto
            pedido_produto = PedidoPorProduto.objects.create(
                pedido=pedido,
                produto=produto,
                quantidade=quantidade,
                valor_unitario=valor_unitario
            )

            # Calcula o valor total do pedido
            valor_total += float(valor_unitario) * int(quantidade)

        # Atualiza o valor total do pedido
        pedido.valor_total = valor_total
        pedido.save()

        return redirect('listar_pedidos')
    else:
        fornecedores = Fornecedor.objects.all()
        produtos = Produtos.objects.all()

        return render(request, 'pedidos/cadastrar_pedidos.html', {
            'fornecedores': fornecedores,
            'produtos': produtos
        })
    
@login_required
def pedidos_dashboard(request):
    data_inicio = request.GET.get('data_inicio')
    data_fim = request.GET.get('data_fim')
    
    if data_inicio and data_fim:
        try:
            data_inicio = datetime.strptime(data_inicio, '%Y-%m-%d').date()
            data_fim = datetime.strptime(data_fim, '%Y-%m-%d').date()
        except (ValueError, TypeError):
            data_inicio = now().date() - timedelta(days=30)
            data_fim = now().date()
    else:
        data_inicio = now().date() - timedelta(days=30)
        data_fim = now().date()
    
    # Dados para gráfico de valor total por dia
    pedidos_por_dia = Pedidos.objects.filter(
        data_pedido__gte=data_inicio,
        data_pedido__lte=data_fim
    ).values('data_pedido').annotate(
        total_valor=Sum('valor_total'),
        total_pedidos=Count('id')
    ).order_by('data_pedido')
    
    # Preparar dados para Chart.js
    datas = [item['data_pedido'].strftime('%Y-%m-%d') for item in pedidos_por_dia]
    valores = [float(item['total_valor']) if item['total_valor'] else 0 for item in pedidos_por_dia]
    qtd_pedidos = [item['total_pedidos'] for item in pedidos_por_dia]
    
    # Item mais comprado no período
    item_mais_comprado = PedidoPorProduto.objects.filter(
        pedido__data_pedido__gte=data_inicio,
        pedido__data_pedido__lte=data_fim
    ).values('produto__nome').annotate(
        total_quantidade=Sum('quantidade'),
        total_vendido=Sum(F('quantidade') * F('valor_unitario'))
    ).order_by('-total_quantidade').first()
    
    context = {
        'data_inicio': data_inicio.strftime('%Y-%m-%d'),
        'data_fim': data_fim.strftime('%Y-%m-%d'),
        'datas_json': json.dumps(datas),
        'valores_json': json.dumps(valores),
        'qtd_pedidos_json': json.dumps(qtd_pedidos),
        'item_mais_comprado': item_mais_comprado,
    }
    
    return render(request, 'pedidos/dashboard.html', context)
