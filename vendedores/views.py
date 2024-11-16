from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.template import loader, RequestContext
from .models import Fornecedor
from django.contrib.auth.decorators import login_required

@login_required
def fornecedores(request):
    template = loader.get_template('fornecedores/index.html')
    return HttpResponse(template.render())

@login_required
def listar_fornecedores(request):
    fornecedores = Fornecedor.objects.all()
    return render(request, 'fornecedores/lista_fornecedores.html', {'fornecedores': fornecedores})

@login_required
def novo_fornecedor(request):
    if request.method == 'POST':
        fornecedor = Fornecedor(
            nome = request.POST['nome'],
            cnpj = request.POST['cnpj'],
            ie = request.POST['ie'],
            endereco = request.POST['endereco'],
            bairro = request.POST['bairro'],
            cidade = request.POST['cidade'],
            estado = request.POST['estado'],
            pais = request.POST['pais'],
            cep = request.POST['cep'],
            telefone = request.POST['telefone'],
            email = request.POST['email']
        )
        fornecedor.save()
        return redirect('listar_fornecedores')
    return render(request, 'fornecedores/novo_fornecedor.html')

@login_required
def editar_fornecedor(request, pk):
    fornecedor = get_object_or_404(Fornecedor, pk=pk)
    if request.method == 'POST':
        fornecedor.ie = request.POST['ie']
        fornecedor.endereco = request.POST['endereco']
        fornecedor.telefone = request.POST['telefone']
        fornecedor.bairro = request.POST['bairro']
        fornecedor.cidade = request.POST['cidade']
        fornecedor.estado = request.POST['estado']
        fornecedor.pais = request.POST['pais']
        fornecedor.cep = request.POST['cep']
        fornecedor.email = request.POST['email']
        fornecedor.save()
        return redirect('listar_fornecedores')
    return render(request, 'fornecedores/editar_fornecedor.html', {'fornecedor': fornecedor})

@login_required
def remover_fornecedor(request, pk):
    fornecedor = get_object_or_404(Fornecedor, pk=pk)
    if request.method == 'POST':
        fornecedor.delete()
        return redirect('listar_fornecedores')
    return render(request, 'fornecedores/deletar_fornecedor.html', {'fornecedor': fornecedor})
