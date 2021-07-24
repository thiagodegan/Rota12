from django.http import request
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from rota12.models import Entidade
from validate_docbr import CNPJ, CPF
from rota12.cepUtil import valida_cep, consulta

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
            entidade = Entidade.objects.create(Nome=nome, Email=email, Saldo = 0, User=user)
            entidade.save()
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
        bairro = request.POST['bairro']
        endereco = request.POST['endereco']
        numero = request.POST['numero']
        complemento = request.POST['complemento']
        telefone = request.POST['telefone']

        nome_IsValid = True
        nome_message = ""
        tipopessoa_IsValid = True
        tipopessoa_message = ""
        cnpj_IsValid = True
        cnpj_message = ""
        cep_IsValid = True
        cep_message = ""
        estado_IsValid = True
        estado_message = ""
        cidade_IsValid = True
        cidade_message = ""
        bairro_IsValid = True
        bairro_message = True
        endereco_IsValid = True
        endereco_message = ""
        numero_IsValid = True
        numero_message = ""
        telefone_IsValid = True
        telefone_message = ""

        if not nome.strip():
            nome_IsValid = False
            nome_message = "Informe o Nome"
        
        if not tipopessoa.strip():
            tipopessoa_IsValid = False
            tipopessoa_message = "Selecione o Tipo de Pessoa"
        elif tipopessoa != "F" and tipopessoa != "J":
            tipopessoa_IsValid = False
            tipopessoa_message = "Tipo de Pessoa Inválido"

        if not cnpj.strip():
            cnpj_IsValid = False
            cnpj_message = "Informe o CNPJ/CPF"
        elif tipopessoa == "F":
            # #18 VALIDA SE É UM CPF VÁLIDO
            validadorCpf = CPF()
            cnpj = cnpj.strip().replace(".", "").replace("-", "").replace("/", "")
            cnpj = validadorCpf.mask(cnpj)
            if (not validadorCpf.validate(cnpj)):
                cnpj_IsValid = False
                cnpj_message = "CPF Inválido"
        elif tipopessoa == "J":
            # #19 VALIDA SE É UM CNPJ VÁLIDO
            validadorCnpj = CNPJ()
            # Remove formatacao do CNPJ se existir
            cnpj = cnpj.strip().replace(".", "").replace("-", "").replace("/", "")
            cnpj = validadorCnpj.mask(cnpj)
            if (not validadorCnpj.validate(cnpj)):
                cnpj_IsValid = False
                cnpj_message = "CNPJ Inválido"
            
        
        if not cep.strip():
            cep_IsValid = False
            cep_message = "Informe o CEP"
        else:
            # #20 VERIFICAR SE É POSSÍVEL VALIDAR O CEP
            if (valida_cep(cep)):
                enderecoDic = consulta(cep)
                if not enderecoDic.get('erro'):
                    if enderecoDic.get('uf'):
                        estado = enderecoDic.get('uf')
                    if enderecoDic.get('localidade'):
                        cidade = enderecoDic.get('localidade')
                    if enderecoDic.get('bairro'):
                        bairro = enderecoDic.get('bairro')
                    if not endereco.strip():
                        endereco = enderecoDic.get('endereco')
            else:
                cep_IsValid = False
                cep_message = "CEP Inválido"

        if not estado.strip():
            estado_IsValid = False
            estado_message = "Informe o Estado"
        
        if not cidade.strip():
            cidade_IsValid = False
            cidade_message = "Informe a Cidade"
        
        if not bairro.strip():
            bairro_IsValid = False
            bairro_message = "Informe o Bairro"

        if not endereco.strip():
            endereco_IsValid = False
            endereco_message = "Informe o Endereço"

        if not numero.strip():
            numero_IsValid = False
            numero_message = "Informe o Número"

        if not telefone.strip():
            telefone_IsValid = False
            telefone_message = "Informe o Telefone"

        if (not nome_IsValid or 
            not tipopessoa_IsValid or
            not cnpj_IsValid or
            not cep_IsValid or
            not estado_IsValid or
            not cidade_IsValid or
            not bairro_IsValid or
            not endereco_IsValid or
            not numero_IsValid or
            not telefone_IsValid):
            dados = {
                'nome': nome,
                'nome_IsValid': 'is-valid' if nome_IsValid == True else 'is-invalid',
                'nome_message': nome_message,
                'tipopessoa': tipopessoa,
                'tipopessoa_IsValid': 'is-valid' if tipopessoa_IsValid == True else 'is-invalid',
                'tipopessoa_message': tipopessoa_message,
                'cnpj': cnpj,
                'cnpj_IsValid': 'is-valid' if cnpj_IsValid == True else 'is-invalid',
                'cnpj_message': cnpj_message,
                'cep': cep,
                'cep_IsValid': 'is-valid' if cep_IsValid == True else 'is-invalid',
                'cep_message': cep_message,
                'estado': estado,
                'estado_IsValid': 'is-valid' if estado_IsValid == True else 'is-invalid',
                'estado_message': estado_message,
                'cidade': cidade,
                'cidade_IsValid': 'is-valid' if cidade_IsValid == True else 'is-invalid',
                'cidade_message': cidade_message,
                'bairro': bairro,
                'bairro_IsValid': 'is-valid' if bairro_IsValid == True else 'is-invalid',
                'bairro_message': bairro_message,
                'endereco': endereco,
                'endereco_IsValid': 'is-valid' if endereco_IsValid == True else 'is-invalid',
                'endereco_message': endereco_message,
                'numero': numero,
                'numero_IsValid': 'is-valid' if numero_IsValid == True else 'is-invalid',
                'numero_message': numero_message,
                'complemento': complemento,
                'telefone': telefone,
                'telefone_IsValid': 'is-valid' if telefone_IsValid == True else 'is-invalid',
                'telefone_message': telefone_message,
            }
            print(dados)
            return render(request, 'usuarios/perfil.html', dados)

        user = request.user

        user.username = nome
        user.entidade.Nome = nome
        user.entidade.TipoPessoa = tipopessoa
        user.entidade.CpfCnpj = cnpj
        user.entidade.Estado = estado
        user.entidade.Cidade = cidade
        user.entidade.Bairro = bairro
        user.entidade.Endereco = endereco
        user.entidade.Numero = numero
        user.entidade.Complemento = complemento
        user.entidade.Cep = cep
        user.entidade.Telefone = telefone

        user.save()
        user.entidade.save()
        return redirect('index')
    return render(request, 'usuarios/perfil.html')

@login_required
def alterasenha(request):
    if request.method == 'POST':
        email = request.POST['email']
        senha = request.POST['password']
        senha2 = request.POST['confpassword']

        email_IsValid = True
        email_message = ""
        senha_IsValid = True
        senha_message = ""
        senha2_IsValid = True
        senha2_message = ""
        currentUser = request.user.username
        if not email.strip():
            email_IsValid = False
            email_message = "Informe o email"
        elif User.objects.filter(email=email).exclude(username=currentUser).exists():
            email_IsValid = False
            email_message = "Email já cadastrado"
        
        if not senha.strip():
            senha_IsValid = False
            senha_message = "Informe a senha"
        
        if not senha2.strip():
            senha2_IsValid = False
            senha2_message = "Informe a senha"
        elif senha != senha2:
            senha2_IsValid = False
            senha2_message = "Senhas não conferem"
        
        if (not email_IsValid or
            not senha_IsValid or
            not senha2_IsValid):
            dados = {
                'email': email,
                'email_IsValid': 'is-valid' if email_IsValid == True else 'is-invalid',
                'email_message': email_message,
                'senha': senha,
                'senha_IsValid': 'is-valid' if senha_IsValid == True else 'is-invalid',
                'senha_message': senha_message,
                'senha2': senha2,
                'senha_IsValid': 'is_valid' if senha2_IsValid == True else 'is-invalid',
                'senha_message': senha2_message
            }
            print(dados)
            return render(request, 'usuarios/alterasenha.html', dados)
        
        user = request.user
        user.email = email
        user.set_password(senha)
        user.save()
        user.entidade.email = email
        user.entidade.save()
        user = authenticate(request, username=email, password=senha)
        if user is not None:
            auth_login(request, user)
            return redirect('index')
        return redirect('index')

    return render(request, 'usuarios/alterasenha.html')