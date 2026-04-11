from django.urls import path
from MeuApp import views
from jogos import views as jogos_views

app_name = 'MeuApp'

urlpatterns = [
    path('', views.home, name='homepage'),
    path('conquistas/',jogos_views.conquistas,name='conquistas'),
    path('login/',views.login,name='login'),
    path('registro/',views.registro,name='registro'),
    path('logout/', views.logout_view, name='logout'),
    path('perfil/', views.perfil, name='perfil'),
    path('jornada/', jogos_views.jornada, name='jornada'),
]
