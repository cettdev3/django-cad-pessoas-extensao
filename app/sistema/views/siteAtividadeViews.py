from django.shortcuts import render, redirect

from sistema.models.atividade import Atividade
from sistema.models.acao import Acao
from sistema.models.atividadeSection import AtividadeSection
from sistema.models.atividadeCategoria import AtividadeCategoria
from sistema.models.dpEvento import DpEvento
from sistema.models.departamento import Departamento
from sistema.models.membroExecucao import MembroExecucao
from django.contrib.auth.decorators import login_required
from django.db.models import Q, Prefetch
from ..serializers.atividadeSerializer import AtividadeSerializer
from ..serializers.atividadeSectionSerializer import AtividadeSectionSerializer
import requests
import json
from django.http import JsonResponse
from rest_framework.authtoken.models import Token
from django.db.models import Prefetch
from django.core.exceptions import ObjectDoesNotExist

@login_required(login_url="/auth-user/login-user")
def atividadesTable(request):
    nome = request.GET.get("nome")
    acao_id = request.GET.get("acao_id")
    evento_id = request.GET.get("dp_evento_id")
    atividades = Atividade.objects
    if acao_id:
        atividades = atividades.filter(acao__id=acao_id)
    if nome:
        atividades = atividades.filter(
            Q(descricao__contains=nome) | Q(tipoAtividade__nome__contains=nome)
        )

    atividades = atividades.prefetch_related("servico_set").all()
    atividades = AtividadeSerializer(atividades, many=True).data
    return render(
        request, "atividades/atividadesTabela.html", {"atividades": atividades}
    )


@login_required(login_url="/auth-user/login-user")
def atividadesDpEventoTable(request):
    departamento_id = request.GET.get("departamento_id", None)
    nome = request.GET.get("nome", None)
    categoria = request.GET.get("categoria", None)
    responsavel_id = request.GET.get("responsavel_id", None)
    data_fim = request.GET.get("data_fim", None)
    evento_id = request.GET.get("dp_evento_id")

    queryset = Atividade.objects.all()
    if departamento_id is not None and departamento_id != "":
        queryset = queryset.filter(departamento_id=departamento_id)

    if nome is not None and nome != "":
        queryset = queryset.filter(nome__icontains=nome)

    if categoria is not None and categoria != "":
        queryset = queryset.filter(atividadeCategorias__id=categoria)

    if responsavel_id is not None and responsavel_id != "":
        queryset = queryset.filter(responsavel_id=responsavel_id)

    if data_fim is not None and data_fim != "":
        queryset = queryset.filter(data_realizacao_fim=data_fim)

    prefetch = Prefetch("atividade_set", queryset=queryset)
    atividadeSections = AtividadeSection.objects.filter(evento__id=evento_id)

    atividadeSections = (
        atividadeSections.order_by("order").all().prefetch_related(prefetch)
    )

    categorias = AtividadeCategoria.objects.all()

    data = {}
    data["membrosExecucao"] = MembroExecucao.objects.filter(evento__id=evento_id).all()
    data["evento_id"] = evento_id
    data["atividadeSections"] = AtividadeSectionSerializer(
        atividadeSections, many=True
    ).data
    data["categorias"] = categorias
    data["departamentos"] = Departamento.objects.all()

    return render(request, "atividades/atividadesTabela.html", data)


@login_required(login_url="/auth-user/login-user")
def atividadeModal(request):
    acao_id = request.GET.get("acao_id")
    evento_id = request.GET.get("dp_evento_id")
    data = {}
    if acao_id:
        acao = Acao.objects.get(id=acao_id)
        data["acao"] = acao
    if evento_id:
        evento = DpEvento.objects.get(id=evento_id)
        data["evento"] = evento
    return render(request, "atividades/atividadesModal.html", data)


@login_required(login_url="/auth-user/login-user")
def atividadeSelect(request):
    evento_id = request.GET.get("evento_id")
    data = {}
    if evento_id:
        evento = DpEvento.objects.get(id=evento_id)
        data["atividades"] = Atividade.objects.filter(evento=evento)
    else:
        data["atividades"] = Atividade.objects.all()
    return render(request, "atividades/atividadeSelect.html", data)


@login_required(login_url="/auth-user/login-user")
def deleteAtividade(request, atividade_id):
    token, created = Token.objects.get_or_create(user=request.user)
    headers = {"Authorization": "Token " + token.key}
    url = "http://localhost:8000/atividades/" + str(atividade_id)
    response = requests.delete(url, headers=headers)
    return JsonResponse(
        {"status": response.status_code, "message": response.content.decode()}
    )


@login_required(login_url="/auth-user/login-user")
def saveAtividade(request):
    token, created = Token.objects.get_or_create(user=request.user)
    headers = {"Authorization": "Token " + token.key}
    body = json.loads(request.body)
    response = requests.post(
        "http://localhost:8000/atividades", json=body, headers=headers
    )
    atividade = json.loads(response.content)
    categorias = AtividadeCategoria.objects.all()
    thumbnailStyle = True

    data = {}
    eventoId = atividade.get("evento").get("id")
    data["membrosExecucao"] = MembroExecucao.objects.filter(evento__id=eventoId).all()
    data["atividade"] = atividade
    data["evento_id"] = eventoId
    data["categorias"] = categorias
    data["thumbnailStyle"] = thumbnailStyle
    data["fromCreate"] = True
    data["departamentos"] = Departamento.objects.all()
    return render(request, "atividades/atividade-row.html", data)


@login_required(login_url="/auth-user/login-user")
def editarAtividade(request, atividade_id):
    token, created = Token.objects.get_or_create(user=request.user)
    headers = {"Authorization": "Token " + token.key}
    body = json.loads(request.body)
    replaceContainerId = body.get("replaceContainerId", None)
    containerId = body.get("containerId", None)
    template = body.get("template") if body.get("template") else "atividade-row.html"
    response = requests.put(
        "http://localhost:8000/atividades/" + str(atividade_id),
        json=body,
        headers=headers,
    )
    atividade = json.loads(response.content)
    categorias = AtividadeCategoria.objects.all()
    thumbnailStyle = True
    data = {}

    eventoId = atividade.get("evento").get("id")
    data["membrosExecucao"] = MembroExecucao.objects.filter(evento__id=eventoId).all()
    data["atividade"] = atividade
    data["evento_id"] = eventoId
    data["categorias"] = categorias
    data["thumbnailStyle"] = thumbnailStyle
    data["departamentos"] = Departamento.objects.all()
    data['replaceContainerId'] = replaceContainerId
    data['containerId'] = containerId
    return render(request, "atividades/" + template, data)


@login_required(login_url="/auth-user/login-user")
def getAtividadeDrawer(request, atividade_id):
    token, created = Token.objects.get_or_create(user=request.user)
    headers = {"Authorization": "Token " + token.key}
    response = requests.get(
        "http://localhost:8000/atividades/" + str(atividade_id), headers=headers
    )
    atividade = json.loads(response.content)
    categorias = AtividadeCategoria.objects.all()
    thumbnailStyle = True

    return render(
        request,
        "atividades/atividade-drawer.html",
        {
            "atividade": atividade,
            "categorias": categorias,
            "thumbnailStyle": thumbnailStyle,
        },
    )

@login_required(login_url="/auth-user/login-user")
def atividadeForm(request):
    model_id = request.GET.get("model_id")
    context = {}
    if model_id:
        try:
            atividade = Atividade.objects.get(pk=model_id)
            context["atividade"] = atividade
        except ObjectDoesNotExist:
            return JsonResponse({"message": "Atividade não encontrada"}, status=400)
    return render(
        request,
        "projetosCotec/atividadeForm.html",
        context,
    )