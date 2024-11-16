from django.shortcuts import render
from django.template import loader, RequestContext
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from .models import Estoque
from pedidos.models import Produtos
from django.contrib.auth.decorators import login_required

@login_required
def estoque(request):
    return render(request, 'estoque/index.html')

@login_required
def listar_estoque(request):
    estoque = Estoque.objects.select_related('produto').all()  # Carrega os produtos junto com o estoque
    return render(request, 'estoque/listar_estoque.html', {'estoque': estoque})

@login_required
def cadastrar_estoque(request):
    if request.method == 'POST':
        # Captura os dados do formulário
        nome = request.POST.get('nome')
        quantidade = int(request.POST.get('quantidade'))

        # Cria o produto na tabela Produtos
        produto = Produtos.objects.create(nome=nome)

        # Cria o registro na tabela Estoque com o produto e quantidade
        Estoque.objects.create(produto=produto, quantidade=quantidade)

        return redirect('listar_estoque')  # Redireciona para uma página de sucesso ou lista de produtos
    return render(request, 'estoque/cadastrar_produto.html')

@login_required
def editar_produto(request, produto):
    estoque = get_object_or_404(Estoque, produto=produto)
    infoproduto = estoque.produto 
    if request.method == "POST":
        nova_quantidade = request.POST.get("quantidade")
        novo_nome = request.POST.get('nome-produto')

        if nova_quantidade:
            infoproduto.nome = novo_nome
            infoproduto.save()
            estoque.quantidade = int(nova_quantidade)
            estoque.save()
            return redirect('listar_estoque')

    return render(request, "estoque/editar_produto.html", {"estoque": estoque})

@login_required
def remover_produto(request, produto):
    estoque = get_object_or_404(Estoque, produto=produto)
    infoproduto = estoque.produto
    if request.method == 'POST':
        estoque.delete()
        infoproduto.delete()
        return redirect('listar_estoque')
    return render(request, 'estoque/remover_produto.html', {'estoque': estoque})