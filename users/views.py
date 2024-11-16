from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.hashers import make_password
from django.contrib.auth import update_session_auth_hash
from .models import Usuario

def is_admin(user):
    return user.is_authenticated and user.perfil == Usuario.ADMIN

@user_passes_test(is_admin)
@login_required
def usuarios(request):
    return render(request, 'users/index.html')

@user_passes_test(is_admin)
@login_required
def listar_usuarios(request):
    usuarios = Usuario.objects.all()
    return render(request, 'users/listar_usuarios.html', {'usuarios': usuarios})

def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        # Autentica o usuário
        user = authenticate(request, email=email, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')  # Redireciona para a página inicial após login
        else:
            messages.error(request, "Credenciais inválidas.")
            return redirect('login')  # Redireciona de volta para a página de login
    return render(request, 'users/login.html')

@user_passes_test(is_admin)
@login_required
def novo_usuario(request):
    if request.method == 'POST':
        # Captura dados do formulário enviados pelo método POST
        username = request.POST.get('username')
        email = request.POST.get('email')
        perfil = request.POST.get('perfil')
        senha_temporaria = request.POST.get('senha_temporaria')
        
        # Valida os campos (exemplo: email único)
        if Usuario.objects.filter(email=email).exists():
            return render(request, 'users/novo_usuario.html', {'error': 'Email já cadastrado'})

        # Cria o novo usuário com a senha temporária
        usuario = Usuario(
            username=username,
            email=email,
            perfil=perfil,
            password=make_password(senha_temporaria),  # Define a senha temporária
            is_temporary_password=True  # Marca a senha como temporária
        )
        usuario.save()
        return redirect('usuarios')  # Redireciona para uma página de sucesso

    return render(request, 'users/novo_usuario.html')

@login_required
def alterar_senha_inicial(request):
    usuario = request.user
    if not usuario.is_temporary_password:
        return redirect('home')  # Redireciona se a senha já tiver sido alterada

    if request.method == 'POST':
        nova_senha = request.POST.get('nova_senha')
        usuario.set_password(nova_senha)
        usuario.is_temporary_password = False  # Define que a senha não é mais temporária
        usuario.save()
        update_session_auth_hash(request, usuario)  # Mantém o usuário logado
        return redirect('home')
    
    return render(request, 'users/altera_senha_inicial.html')
