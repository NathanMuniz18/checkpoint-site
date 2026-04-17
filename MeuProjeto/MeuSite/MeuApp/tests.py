from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.conf import settings
from django.core import mail
from django.test import TestCase, override_settings
from django.urls import reverse
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

TEST_MIDDLEWARE = [
    middleware
    for middleware in settings.MIDDLEWARE
    if middleware != "whitenoise.middleware.WhiteNoiseMiddleware"
]


@override_settings(
    EMAIL_BACKEND="django.core.mail.backends.locmem.EmailBackend",
    MIDDLEWARE=TEST_MIDDLEWARE,
)
class PasswordResetFlowTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="alexandre",
            email="alexandre@example.com",
            password="SenhaForte@2026",
        )

    def test_recuperar_senha_envia_email_e_redireciona(self):
        response = self.client.post(
            reverse("MeuApp:recuperar_senha"),
            {"email": self.user.email},
        )

        self.assertRedirects(response, reverse("MeuApp:recuperar_senha_enviado"))
        self.assertEqual(len(mail.outbox), 1)
        self.assertIn(self.user.username, mail.outbox[0].body)
        self.assertIn("redefinir-senha", mail.outbox[0].body)

    def test_redefinir_senha_com_token_valido(self):
        uid = urlsafe_base64_encode(force_bytes(self.user.pk))
        token = default_token_generator.make_token(self.user)

        response = self.client.get(
            reverse(
                "MeuApp:redefinir_senha",
                kwargs={"uidb64": uid, "token": token},
            ),
            follow=True,
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Defina sua nova senha")

    def test_redefinir_senha_com_token_invalido(self):
        uid = urlsafe_base64_encode(force_bytes(self.user.pk))

        response = self.client.get(
            reverse(
                "MeuApp:redefinir_senha",
                kwargs={"uidb64": uid, "token": "token-invalido"},
            )
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "link de redefinição é inválido")
