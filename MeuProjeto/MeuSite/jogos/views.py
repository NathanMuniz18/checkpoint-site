from django.shortcuts import render
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import redirect, render
from django.urls import reverse

# Create your views here.

def conquistas(request):
    return render(request, 'jogos/conquistas.html')

def jornada(request):
    return render(request, 'jogos/jornada.html')