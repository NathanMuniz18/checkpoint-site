from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Pessoa

class CadastroForm(UserCreationForm):
    email = forms.EmailField(
        help_text='Informe um email válido',
        label='Email'
    )

    class Meta:
        model = User
        # Não coloque as senhas aqui! O UserCreationForm já lida com elas.
        fields = ['username', 'email'] 

class PessoaForm(forms.ModelForm):
    # As definições personalizadas ficam FORA da classe Meta
    foto = forms.URLField(required=False)
    bio = forms.CharField(required=False)

    class Meta:
        model = Pessoa
        fields = ['foto', 'bio']