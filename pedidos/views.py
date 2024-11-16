from decimal import Decimal
from django.shortcuts import render
from django.template import loader, RequestContext
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from vendedores.models import Fornecedor
from .models import Produtos, Pedidos, PedidoPorProduto
from django.contrib.auth.decorators import login_required

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