# 🎮 Checkpoint

> Sua jornada gamer, organizada em um só lugar.

Checkpoint é uma aplicação web desenvolvida em **Django** que permite ao usuário registrar e acompanhar sua jornada nos jogos: pesquise títulos via API RAWG, adicione-os à sua biblioteca pessoal, defina um status e registre suas horas jogadas.


## 🎯 Escopo do Projeto

O Checkpoint nasceu como um projeto acadêmico com o objetivo de desenvolver uma aplicação web completa com Django, cobrindo desde autenticação de usuários até integração com APIs externas.

### O que foi desenvolvido

O projeto foi construído em duas frentes principais, divididas em dois apps Django:

**`MeuApp` — Autenticação e Perfil**

O primeiro app cobre toda a camada de identidade do usuário. Foram implementados o fluxo de registro e login com formulários customizados sobre os padrões do Django, edição de perfil com campos de username, e-mail, bio e foto via URL (com normalização automática de diferentes formatos de URL), e um fluxo completo de recuperação e redefinição de senha via e-mail com tokens temporários. Também foi implementada a exclusão de conta autenticada.

**`jogos` — Jornada e Conquistas**

O segundo app é o coração do produto. Nele, o usuário autenticado acessa sua jornada, pesquisa jogos pelo nome diretamente na API RAWG (sem necessidade de JavaScript no cliente), adiciona títulos à sua biblioteca pessoal, define o status do jogo e registra horas jogadas. Os dados dos jogos consultados são persistidos localmente para evitar chamadas repetidas à API.

A **página de conquistas** foi desenvolvida com layout visual completo, mas **não possui lógica de backend implementada** — é meramente ilustrativa e representa uma funcionalidade planejada para versões futuras.

---

## 🛠️ Stack e Arquitetura

| Camada | Tecnologia |
|---|---|
| Linguagem | Python 3.12 |
| Framework Web | Django 6.0.3 |
| Banco de Dados | SQLite3 |
| Arquivos Estáticos | WhiteNoise |
| Servidor (produção) | Gunicorn |
| Containerização | Docker + Docker Compose |
| API Externa | RAWG Video Games Database |

### Apps Django

- **`MeuApp`** — autenticação, home, perfil e recuperação de senha
- **`jogos`** — jornada pessoal e conquistas (layout)

---

## ✅ Funcionalidades

### MeuApp

- Home diferenciada para visitante e usuário autenticado
- Registro com `UserCreationForm` customizado
- Login com `AuthenticationForm`
- Edição de perfil: username, e-mail, bio e foto por URL
- Normalização de URL de foto (aceita `http`, `https`, `data:image`, `blob` e caminhos locais)
- Fluxo completo de recuperação/redefinição de senha por e-mail
- Exclusão de conta

### jogos

- Página de jornada protegida por login (`@login_required`)
- Busca de jogos por nome na API RAWG (server-side)
- Adição de jogo à biblioteca pessoal
- Atualização de status e horas jogadas
- Remoção de jogo da jornada
- Página de conquistas com layout visual *(sem lógica de backend — meramente ilustrativa)*

---

## 📖 Manual do Usuário

### 1. Criar uma conta

Acesse `(https://checkpoint-site.onrender.com)` e preencha o formulário com nome de usuário, e-mail e senha. Após o cadastro, você será redirecionado automaticamente para a página inicial já autenticado.

### 2. Fazer login e logout

- **Login:** acesse `/login/` e informe seu usuário e senha.
- **Logout:** clique na opção de sair disponível no menu. Você será desconectado e redirecionado para a home de visitante.

### 3. Editar seu perfil

Acesse `/perfil/` para atualizar:

- **Username** — seu nome de exibição
- **E-mail** — endereço de contato
- **Bio** — uma breve descrição sobre você
- **Foto** — URL de uma imagem de perfil (o sistema aceita links `http://`, `https://`, `data:image`, `blob:` e caminhos locais)

### 4. Recuperar a senha

Caso esqueça sua senha:

1. Acesse `/recuperar-senha/` e informe seu e-mail.
2. Você receberá um e-mail com um link de redefinição.
3. Clique no link, defina a nova senha e confirme.
4. Após a conclusão, faça login normalmente.

### 5. Explorar sua Jornada

Acesse `/MeuApp/jornada/` (disponível apenas para usuários logados).

**Buscar um jogo:**

1. No campo de busca, digite o nome do jogo desejado.
2. Clique em **Buscar**. Os resultados virão da API RAWG com capa, nome e plataforma.

**Adicionar um jogo à biblioteca:**

1. Nos resultados da busca, clique em **Adicionar** ao lado do jogo desejado.
2. O jogo aparecerá na sua lista pessoal.

**Atualizar status e horas jogadas:**

Em cada jogo da sua lista, você pode definir:

| Status | Descrição |
|---|---|
| `Vou jogar` | Jogo na fila, ainda não iniciado |
| `Tô jogando` | Jogo em andamento |
| `Já zerei` | Jogo concluído |
| `Desisti` | Jogo abandonado |

Informe também as **horas jogadas** e salve as alterações.

**Remover um jogo:**

Clique em **Remover** para excluir o jogo da sua jornada. Essa ação é irreversível.

### 6. Página de Conquistas

Acesse `/MeuApp/conquistas/` para visualizar o layout da área de conquistas.

> ⚠️ **Esta página é meramente ilustrativa.** O sistema de conquistas não possui lógica de backend implementada — os dados exibidos são estáticos e não refletem o progresso real do usuário. A funcionalidade está planejada para versões futuras.

### 7. Excluir a conta

Em `/excluir-conta/`, é possível remover permanentemente sua conta. Todos os seus dados, incluindo os jogos da jornada, serão apagados. **Essa ação não pode ser desfeita.**

---

## 📁 Estrutura de Pastas

```text
checkpoint-site/
├── docker-compose.yml
├── README.md
└── MeuProjeto/
    ├── Dockerfile
    ├── requirements.txt
    └── MeuSite/
        ├── manage.py
        ├── db.sqlite3
        ├── MeuSite/
        │   ├── settings.py
        │   ├── urls.py
        │   ├── wsgi.py
        │   └── asgi.py
        ├── MeuApp/
        │   ├── models.py
        │   ├── forms.py
        │   ├── views.py
        │   ├── urls.py
        │   ├── tests.py
        │   ├── templates/MeuApp/
        │   └── static/MeuApp/
        └── jogos/
            ├── models.py
            ├── views.py
            ├── urls.py
            ├── migrations/
            ├── templates/jogos/
            └── static/jogos/
```

---


## 🗄️ Banco de Dados e Migrações

O banco padrão é SQLite, localizado em `MeuProjeto/MeuSite/db.sqlite3`.

---

## 🗺️ Rotas da Aplicação

### App `MeuApp` (raiz `/`)

| Rota | Descrição |
|---|---|
| `/` | Home |
| `/login/` | Login |
| `/registro/` | Cadastro |
| `/logout/` | Logout |
| `/perfil/` | Edição de perfil |
| `/excluir-conta/` | Exclusão de conta |
| `/recuperar-senha/` | Solicitar redefinição de senha |
| `/recuperar-senha/enviado/` | Confirmação de envio |
| `/redefinir-senha/<uidb64>/<token>/` | Redefinição de senha |
| `/redefinir-senha/concluida/` | Finalização |

### App `jogos` (prefixo `/MeuApp/`)

| Rota | Descrição |
|---|---|
| `/MeuApp/jornada/` | Biblioteca pessoal de jogos |
| `/MeuApp/conquistas/` | Página de conquistas *(apenas layout)* |

> ⚠️ `/MeuApp/` sozinho **não é uma rota válida** no estado atual da aplicação.

---

## 🧩 Modelos de Dados

### `MeuApp.Pessoa`

Estende o `User` do Django com dados de perfil via `OneToOneField`.

| Campo | Tipo | Descrição |
|---|---|---|
| `usuario` | OneToOne → User | Referência ao usuário Django |
| `foto` | URLField (opcional) | URL da foto de perfil |
| `bio` | TextField (opcional) | Descrição pessoal |

### `jogos.Jogo`

Catálogo local de jogos referenciados da RAWG.

| Campo | Tipo | Descrição |
|---|---|---|
| `rawg_id` | IntegerField (único) | ID do jogo na RAWG |
| `nome` | CharField | Nome do jogo |
| `capa_url` | URLField | URL da imagem de capa |
| `plataforma` | CharField | Plataformas disponíveis |
| `slug` | SlugField | Slug do jogo |
| `criado_em` | DateTimeField | Timestamp de criação |
| `atualizado_em` | DateTimeField | Timestamp de atualização |

### `jogos.JogoUsuario`

Tabela de associação entre usuário e jogo (biblioteca pessoal).

| Campo | Tipo | Descrição |
|---|---|---|
| `usuario` | ForeignKey → User | Dono da entrada |
| `jogo` | ForeignKey → Jogo | Jogo associado |
| `status` | CharField (choices) | `vou_jogar`, `to_jogando`, `ja_zerei`, `desisti` |
| `horas_jogadas` | PositiveIntegerField | Total de horas jogadas |
| `criado_em` | DateTimeField | Timestamp de criação |
| `atualizado_em` | DateTimeField | Timestamp de atualização |

---

## 🎮 Integração com a API RAWG

A busca de jogos utiliza a [RAWG Video Games Database API](https://rawg.io/apidocs).

- **Endpoint:** `https://api.rawg.io/api/games`
- **Busca:** via query string `?search=<termo>`
- **Chave:** lida de `settings.RAWG_API_KEY` (configurada no `.env`)
- **Fluxo:** o usuário busca pelo nome → o backend consulta a RAWG → os resultados são renderizados no template → ao adicionar, os dados essenciais do jogo são persistidos localmente no SQLite

---

## 📧 Recuperação de Senha por E-mail

Implementado com as views nativas do Django (`django.contrib.auth.views`).

**Fluxo:**

1. Usuário acessa `/recuperar-senha/` e informa o e-mail cadastrado.
2. O sistema envia um e-mail com link tokenizado e com validade limitada.
3. O usuário acessa o link em `/redefinir-senha/<uidb64>/<token>/`.
4. Define a nova senha e o fluxo é concluído em `/redefinir-senha/concluida/`.

**Templates de e-mail:**

```
MeuApp/templates/MeuApp/emails/
├── recuperacao_senha_assunto.txt
├── recuperacao_senha_email.txt
└── recuperacao_senha_email.html
```
---

## 🚀 Melhorias Futuras

- [ ] Implementar lógica real de conquistas baseada em horas/status dos jogos
- [ ] Adicionar paginação e cache para os resultados da busca RAWG
- [ ] Cobrir o app `jogos` com testes automatizados
- [ ] Migrar para PostgreSQL em ambiente de produção

---
OBS: esse readme e alguma coisas do codigo foram feitas com ajuda de ia 
<p align="center">
  Desenvolvido por <strong>Alexandre</strong> e <strong>Nathan</strong>
</p>
