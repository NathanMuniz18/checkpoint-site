from django.contrib.auth import login as auth_login
from django.contrib.auth import logout
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import redirect, render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from .forms import CadastroForm, PerfilForm, PessoaForm
from .models import Pessoa


def home(request):
    pessoa = None
    if request.user.is_authenticated:
        pessoa = Pessoa.objects.filter(usuario=request.user).first()

    return render(
        request,
        'MeuApp/home.html',
        {
            'pessoa': pessoa,
        },
    )


def perfil(request):
    """Exibe o perfil do usuário autenticado e processa edição via POST."""
    if not request.user.is_authenticated:
        return redirect('MeuApp:login')

    pessoa, _ = Pessoa.objects.get_or_create(usuario=request.user)

    if request.method == 'POST':
        form = PerfilForm(request.POST, user=request.user, pessoa=pessoa)

        if form.is_valid():
            form.save()
            return redirect(f"{reverse('MeuApp:perfil')}?salvo=1")
    else:
        form = PerfilForm(user=request.user, pessoa=pessoa)

    return render(
        request,
        'MeuApp/perfil.html',
        {
            'pessoa': pessoa,
            'form': form,
            'perfil_salvo': request.GET.get('salvo') == '1',
        },
    )


def segundaPagina(request):
    return render(request, 'MeuApp/segunda.html')


def conquistas(request):
    return render(request, 'MeuApp/conquistas.html')



def login(request):
    # Se o usuário clicou no botão de Entrar (enviou os dados)
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)

        if form.is_valid():
            # Pega o usuário validado e faz o login no sistema
            usuario = form.get_user()
            auth_login(request, usuario)
            return redirect('MeuApp:homepage')  # Manda pra página inicial após logar
    else:
        # Se ele só acessou a página, mostra o formulário vazio
        form = AuthenticationForm()

    return render(request, 'MeuApp/login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('MeuApp:homepage')


@login_required
def excluir_conta(request):
    if request.method == 'POST':   # só age se veio do formulário
        user = request.user        # pega o usuário logado
        logout(request)            # desloga primeiro
        user.delete()              # depois deleta do banco
        return redirect('MeuApp:homepage')  # manda pra home
    return redirect('MeuApp:perfil')  # se não foi POST, volta pro perfil


def registro(request):
    if request.method == 'POST':
        print('\n--- 1. O BOTÃO FOI CLICADO E O POST CHEGOU ---')

        form_usuario = CadastroForm(request.POST)
        form_pessoa = PessoaForm(request.POST, request.FILES)  # Lembre-se do request.FILES se for ter foto

        if form_usuario.is_valid() and form_pessoa.is_valid():
            print('--- 2. SUCESSO: OS DOIS FORMULÁRIOS SÃO VÁLIDOS ---')
            usuario = form_usuario.save()
            pessoa = form_pessoa.save(commit=False)
            pessoa.usuario = usuario
            pessoa.save()
            auth_login(request, usuario)
            return redirect('MeuApp:homepage')
        else:
            print('--- 2. FALHA: O FORMULÁRIO TEM ERROS ---')
            print('Erros do Usuário:', form_usuario.errors)
            print('Erros da Pessoa:', form_pessoa.errors)

    else:
        form_usuario = CadastroForm()
        form_pessoa = PessoaForm()

    return render(
        request,
        'MeuApp/registro.html',
        {
            'form_usuario': form_usuario,
            'form_pessoa': form_pessoa,
        },
    )

def jornada(request):
    pessoa = None
    if request.user.is_authenticated:
        pessoa = Pessoa.objects.filter(usuario=request.user).first()

    return render(
        request,
        'MeuApp/jornada.html',
        {
            'pessoa': pessoa,
        },
    )
