from django.urls import path
from MeuApp import views

app_name = 'MeuApp'

urlpatterns = [
    path('', views.home, name='homepage'),
    path('SegundaPagina/',views.segundaPagina,name='segunda'),
    path('catalogo/',views.catalogo,name='catalogo'),
    path('login/',views.login,name='login'),
    path('registro/',views.registro,name='registro'),
    path('logout/', views.logout_view, name='logout'),
    path('perfil/', views.perfil, name='perfil'),
    path('noticias/', views.noticias, name='noticias'),
    
]
