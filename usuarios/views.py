from django.http import request
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from rota12.models import Entidade

# Create your views here.
def cadastro(request):
    print('Entrou na def cadastro')
    if request.method == 'POST':
        nome = request.POST['nome']
        email = request.POST['email']
        senha = request.POST['password']
        senha2 = request.POST['password2']
        
        nome_message = ""
        nome_IsValid = True
        if not nome.strip():
            nome_IsValid = False
            nome_message = "Informe o nome"
        
        email_message = ""
        email_IsValid = True
        if not email.strip():
            email_IsValid = False
            email_message = "Informe o email"
        elif User.objects.filter(email=email).exists():
            email_IsValid = False
            email_message = "Email já cadastrado"
        
        senha_message = ""
        senha_IsValid = True
        if not senha.strip():
            senha_IsValid = False
            senha_message = "Informe a senha"

        senha2_message = ""
        senha2_IsValid = True
        if not senha2.strip():
            senha2_IsValid = False
            senha2_message = "Informe a confirmação de senha"

        
        senhaDivergente = senha2 != senha

        if senhaDivergente:
            senha2_message = "Senhas não conferem"

        if senhaDivergente:
            senha2_IsValid = False
        
        if not nome_IsValid or not email_IsValid or not senha_IsValid or not senha2_IsValid or senhaDivergente:
            dados = {
                'nome': nome,
                'nome_IsValid': 'is-valid' if nome_IsValid == True else 'is-invalid',
                'nome_message': nome_message,
                'email': email,
                'email_IsValid': 'is-valid' if email_IsValid == True else 'is-invalid',
                'email_message': email_message,
                'senha': senha,
                'senha_IsValid': 'is-valid' if senha_IsValid == True else 'is-invalid',
                'senha_message': senha_message,
                'senha2': senha2,
                'senha2_IsValid': 'is-valid' if senha2_IsValid == True else 'is-invalid',
                'senha2_message': senha2_message,
                'diferente': senhaDivergente
            }
            print(dados)
            return render(request, 'usuarios/cadastro.html', dados)
        else:
            user = User.objects.create_user(username=nome, email=email, password=senha)
            user.save()
            user = authenticate(request, username=email, password=senha)
            if user is not None:
                auth_login(request, user)
                return redirect('index')
            else:
                return(request, 'usuarios/cadastro.html')
    else:
        return render(request, 'usuarios/cadastro.html')

def login(request):
    print('Entrou no login')
    if request.method == 'POST':
        print('Entrou no login como POST')
        email = request.POST['email']
        senha = request.POST['password']
        next = request.POST['next']
        user = authenticate(request, username=email, password=senha)
        if user is not None:
            print('Encontrou o usuario')
            auth_login(request, user)
            if next.strip():
                return redirect(next)
            return redirect('index')
        else:
            dados = {
                'email': email,
                'password': senha,
                'erro': 'Email ou senha inválidos'
            }
            print(dados)
            return render(request, 'usuarios/login.html', dados)
    else:
        print('Entrou no login como GET')
        return render(request, 'usuarios/login.html')

def logout(request):
    auth_logout(request)
    return redirect('index')

@login_required
def perfil(request):
    if request.method == 'POST':
        nome = request.POST['username']
        tipopessoa = request.POST['tipopessoa']
        cnpj = request.POST['cnpjcpf']
        cep = request.POST['cep']
        estado = request.POST['estado']
        cidade = request.POST['cidade']
        endereco = request.POST['endereco']
        telefone = request.POST['telefone']

        user = request.user

        user.username = nome
        user.entidade.Nome = nome
        user.save()
        user.entidade.save()
    
    return render(request, 'usuarios/perfil.html')
