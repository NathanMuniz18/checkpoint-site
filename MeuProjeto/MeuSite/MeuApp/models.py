from django.db import models
from django.contrib.auth.models import User

class Pessoa(models.Model):
    usuario = models.OneToOneField(
        User, 
        on_delete=models.CASCADE,
        related_name='perfil'
    )
    foto = models.URLField(
        help_text='URL de uma foto de perfil',
        max_length=500,
        blank=True,
        null=True
    )
    bio = models.TextField(
        help_text='Uma breve descrição sobre você',
        blank=True,
        null=True
    )

    def __str__(self):
        return self.usuario.username
