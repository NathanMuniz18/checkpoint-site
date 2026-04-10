from django.shortcuts import render, redirect
from django.contrib.auth import login as auth_login
from .forms import CadastroForm, PessoaForm
from .models import Pessoa
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import logout

def home(request):
    return render(request, 'MeuApp/home.html')

def perfil(request):
    if not request.user.is_authenticated:
        return redirect('MeuApp:login')
    
    pessoa = Pessoa.objects.filter(usuario=request.user).first()
    return render(request, 'MeuApp/perfil.html', {'pessoa': pessoa})

def segundaPagina(request):
    return render(request, 'MeuApp/segunda.html')

def catalogo(request):
    return render(request, 'MeuApp/catalogo.html')

def login(request):
    # Se o usuário clicou no botão de Entrar (enviou os dados)
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        
        if form.is_valid():
            # Pega o usuário validado e faz o login no sistema
            usuario = form.get_user()
            auth_login(request, usuario)
            return redirect('MeuApp:homepage') # Manda pra página inicial após logar
    else:
        # Se ele só acessou a página, mostra o formulário vazio
        form = AuthenticationForm()

    return render(request, 'MeuApp/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('MeuApp:homepage')

def registro(request):
    if request.method == 'POST':
        print("\n--- 1. O BOTÃO FOI CLICADO E O POST CHEGOU ---")
        
        form_usuario = CadastroForm(request.POST)
        form_pessoa = PessoaForm(request.POST, request.FILES) # Lembre-se do request.FILES se for ter foto
        
        if form_usuario.is_valid() and form_pessoa.is_valid():
            print("--- 2. SUCESSO: OS DOIS FORMULÁRIOS SÃO VÁLIDOS ---")
            usuario = form_usuario.save()
            pessoa = form_pessoa.save(commit=False)
            pessoa.usuario = usuario
            pessoa.save()
            auth_login(request, usuario)
            return redirect('MeuApp:homepage')
        else:
            print("--- 2. FALHA: O FORMULÁRIO TEM ERROS ---")
            print("Erros do Usuário:", form_usuario.errors)
            print("Erros da Pessoa:", form_pessoa.errors)
            
    else:
        form_usuario = CadastroForm()
        form_pessoa = PessoaForm()

    return render(request, 'MeuApp/registro.html', {
        'form_usuario': form_usuario,
        'form_pessoa': form_pessoa
    })