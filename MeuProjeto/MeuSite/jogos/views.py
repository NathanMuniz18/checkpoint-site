import json
from urllib.error import URLError
from urllib.parse import urlencode
from urllib.request import urlopen

from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from .models import Jogo, JogoUsuario


RAWG_API_URL = "https://api.rawg.io/api/games"


def _buscar_jogos_rawg(termo_busca):
    api_key = getattr(settings, "RAWG_API_KEY", "").strip()
    if not api_key:
        return [], "RAWG_API_KEY não configurada no settings.py."

    params = urlencode(
        {
            "key": api_key,
            "search": termo_busca,
            "page_size": 8,
        }
    )
    url = f"{RAWG_API_URL}?{params}"

    try:
        with urlopen(url, timeout=8) as resposta:
            payload = json.loads(resposta.read().decode("utf-8"))
    except (URLError, TimeoutError, json.JSONDecodeError):
        return [], "Não foi possível consultar a RAWG agora. Tente novamente."

    jogos = []
    for item in payload.get("results", []):
        rawg_id = item.get("id")
        if not rawg_id:
            continue

        plataformas = []
        for plataforma in item.get("platforms") or []:
            nome_plataforma = (plataforma.get("platform") or {}).get("name")
            if nome_plataforma:
                plataformas.append(nome_plataforma)

        jogos.append(
            {
                "rawg_id": rawg_id,
                "nome": item.get("name", "Sem nome"),
                "capa_url": item.get("background_image") or "",
                "plataforma": ", ".join(plataformas[:3]),
                "slug": item.get("slug", ""),
            }
        )

    return jogos, ""


def conquistas(request):
    return render(request, "jogos/conquistas.html")


@login_required(login_url="MeuApp:login")
def jornada(request):
    if request.method == "POST":
        acao = request.POST.get("action", "")

        if acao == "add":
            rawg_id = request.POST.get("rawg_id", "").strip()
            nome = request.POST.get("nome", "").strip()
            capa_url = request.POST.get("capa_url", "").strip()
            plataforma = request.POST.get("plataforma", "").strip()
            slug = request.POST.get("slug", "").strip()
            status = request.POST.get("status", JogoUsuario.Status.VOU_JOGAR)
            horas = request.POST.get("horas_jogadas", "0").strip()

            if not rawg_id.isdigit() or not nome:
                messages.error(request, "Selecione um jogo válido da busca.")
                return redirect("jogos:jornada")

            if status not in dict(JogoUsuario.Status.choices):
                status = JogoUsuario.Status.VOU_JOGAR

            try:
                horas_jogadas = max(int(horas), 0)
            except ValueError:
                horas_jogadas = 0

            jogo, _ = Jogo.objects.update_or_create(
                rawg_id=int(rawg_id),
                defaults={
                    "nome": nome,
                    "capa_url": capa_url,
                    "plataforma": plataforma,
                    "slug": slug,
                },
            )

            item_biblioteca, created = JogoUsuario.objects.get_or_create(
                usuario=request.user,
                jogo=jogo,
                defaults={
                    "status": status,
                    "horas_jogadas": horas_jogadas,
                },
            )

            if not created:
                item_biblioteca.status = status
                item_biblioteca.horas_jogadas = horas_jogadas
                item_biblioteca.save(update_fields=["status", "horas_jogadas", "atualizado_em"])

            messages.success(request, "Jogo adicionado/atualizado na sua jornada.")
            return redirect("jogos:jornada")

        if acao == "update":
            item_id = request.POST.get("item_id", "").strip()
            status = request.POST.get("status", JogoUsuario.Status.VOU_JOGAR)
            horas = request.POST.get("horas_jogadas", "0").strip()

            if item_id.isdigit():
                item = get_object_or_404(JogoUsuario, id=int(item_id), usuario=request.user)
                if status in dict(JogoUsuario.Status.choices):
                    item.status = status
                try:
                    item.horas_jogadas = max(int(horas), 0)
                except ValueError:
                    item.horas_jogadas = 0
                item.save(update_fields=["status", "horas_jogadas", "atualizado_em"])
                messages.success(request, "Jogo atualizado.")
            else:
                messages.error(request, "Item inválido para atualização.")

            return redirect("jogos:jornada")

        if acao == "delete":
            item_id = request.POST.get("item_id", "").strip()
            if item_id.isdigit():
                item = get_object_or_404(JogoUsuario, id=int(item_id), usuario=request.user)
                item.delete()
                messages.success(request, "Jogo removido da jornada.")
            else:
                messages.error(request, "Item inválido para exclusão.")
            return redirect("jogos:jornada")

    query = request.GET.get("q", "").strip()
    resultados_busca, erro_busca = ([], "")
    if query:
        resultados_busca, erro_busca = _buscar_jogos_rawg(query)

    jogos_salvos = (
        JogoUsuario.objects.select_related("jogo")
        .filter(usuario=request.user)
        .order_by("-atualizado_em")
    )

    return render(
        request,
        "jogos/jornada.html",
        {
            "query": query,
            "resultados_busca": resultados_busca,
            "erro_busca": erro_busca,
            "jogos_salvos": jogos_salvos,
            "status_choices": JogoUsuario.Status.choices,
        },
    )
