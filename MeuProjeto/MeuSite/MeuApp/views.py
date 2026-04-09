from django.shortcuts import render
# Create your views here.

def home(request):
# processamento antes de mostrar a home page
    return render(request, 'MeuApp/home.html')

def segundaPagina(request):
# processamento antes de mostrar a segunda página
    return render(request, 'MeuApp/segunda.html')

def catalogo(request):
    return render(request, 'MeuApp/catalogo.html')

def login(request):
    return render(request, 'MeuApp/login.html')

def registro(request):
    return render(request, 'MeuApp/registro.html')