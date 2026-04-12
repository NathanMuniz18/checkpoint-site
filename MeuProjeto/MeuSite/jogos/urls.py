from jogos import views
from django.urls import path

app_name = 'jogos'

urlpatterns = [
    path('conquistas/', views.conquistas, name='conquistas'),
    path('jornada/', views.jornada, name='jornada'),
]

