from django.conf import settings
from django.contrib.auth import views as auth_views
from django.urls import path, reverse_lazy
from MeuApp import views

app_name = 'MeuApp'

urlpatterns = [
    path('', views.home, name='homepage'),
    path('login/',views.login,name='login'),
    path('registro/',views.registro,name='registro'),
    path('logout/', views.logout_view, name='logout'),
    path('perfil/', views.perfil, name='perfil'),
    path('excluir-conta/', views.excluir_conta, name='excluir_conta'),
    path(
        'recuperar-senha/',
        auth_views.PasswordResetView.as_view(
            template_name='MeuApp/recuperar_senha.html',
            email_template_name='MeuApp/emails/recuperacao_senha_email.txt',
            html_email_template_name='MeuApp/emails/recuperacao_senha_email.html',
            subject_template_name='MeuApp/emails/recuperacao_senha_assunto.txt',
            success_url=reverse_lazy('MeuApp:recuperar_senha_enviado'),
            from_email=settings.DEFAULT_FROM_EMAIL,
        ),
        name='recuperar_senha',
    ),
    path(
        'recuperar-senha/enviado/',
        auth_views.PasswordResetDoneView.as_view(
            template_name='MeuApp/recuperacao_senha_enviada.html',
        ),
        name='recuperar_senha_enviado',
    ),
    path(
        'redefinir-senha/<uidb64>/<token>/',
        auth_views.PasswordResetConfirmView.as_view(
            template_name='MeuApp/redefinir_senha_confirmar.html',
            success_url=reverse_lazy('MeuApp:redefinir_senha_concluida'),
        ),
        name='redefinir_senha',
    ),
    path(
        'redefinir-senha/concluida/',
        auth_views.PasswordResetCompleteView.as_view(
            template_name='MeuApp/redefinir_senha_concluida.html',
        ),
        name='redefinir_senha_concluida',
    ),
]
