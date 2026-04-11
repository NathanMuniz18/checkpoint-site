from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import Pessoa


def _normalize_photo_url(value):
    if value is None:
        return ''

    foto = value.strip()
    if not foto:
        return ''

    if foto.startswith('//'):
        return f'https:{foto}'

    allowed_prefixes = (
        'http://',
        'https://',
        'data:image/',
        'blob:',
        '/static/',
        '/',
        './',
        '../',
    )
    if foto.startswith(allowed_prefixes):
        return foto

    # Quando o usuário cola apenas "site.com/imagem.jpg", completa com https.
    return f'https://{foto}'


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
    foto = forms.CharField(required=False)
    bio = forms.CharField(required=False)

    class Meta:
        model = Pessoa
        fields = ['foto', 'bio']

    def clean_foto(self):
        return _normalize_photo_url(self.cleaned_data.get('foto'))


class PerfilForm(forms.Form):
    username = forms.CharField(
        max_length=150,
        label='Usuário',
        widget=forms.TextInput(attrs={
            'class': 'profile-input',
            'placeholder': 'Digite seu username',
            'autocomplete': 'username',
        }),
    )
    email = forms.EmailField(
        label='Email',
        widget=forms.EmailInput(attrs={
            'class': 'profile-input',
            'placeholder': 'Digite seu email',
            'autocomplete': 'email',
        }),
    )
    bio = forms.CharField(
        required=False,
        label='Bio',
        widget=forms.Textarea(attrs={
            'class': 'profile-textarea',
            'placeholder': 'Conte um pouco sobre você',
            'rows': 5,
        }),
    )
    foto = forms.CharField(
        required=False,
        label='Foto (URL)',
        widget=forms.TextInput(attrs={
            'class': 'profile-input',
            'placeholder': 'https://sua-foto.com/imagem.jpg',
            'autocomplete': 'url',
        }),
    )

    def __init__(self, *args, user=None, pessoa=None, **kwargs):
        self.user = user
        self.pessoa = pessoa
        super().__init__(*args, **kwargs)

        if not self.is_bound and self.user is not None:
            self.initial['username'] = self.user.username
            self.initial['email'] = self.user.email
            if self.pessoa is not None:
                self.initial['bio'] = self.pessoa.bio
                self.initial['foto'] = self.pessoa.foto

    def clean_username(self):
        username = self.cleaned_data['username'].strip()

        if self.user is None:
            return username

        username_em_uso = User.objects.filter(username__iexact=username).exclude(pk=self.user.pk)
        if username_em_uso.exists():
            raise forms.ValidationError('Esse username já está em uso.')

        return username

    def clean_foto(self):
        return _normalize_photo_url(self.cleaned_data.get('foto'))

    def save(self):
        if self.user is None or self.pessoa is None:
            raise ValueError('PerfilForm precisa de user e pessoa para salvar.')

        self.user.username = self.cleaned_data['username']
        self.user.email = self.cleaned_data['email']
        self.user.save(update_fields=['username', 'email'])

        self.pessoa.bio = self.cleaned_data['bio']
        self.pessoa.foto = self.cleaned_data['foto']
        self.pessoa.save(update_fields=['bio', 'foto'])

        return self.user, self.pessoa
