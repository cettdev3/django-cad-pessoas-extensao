from contextlib import redirect_stderr
from pyexpat.errors import messages
from django.shortcuts import render, redirect
from sistema.serializers.escolaSerializer import EscolaSerializer
from sistema.models.avaliacao import Avaliacao
from sistema.models.acao import Acao
from sistema.models.dpEvento import DpEvento
from django.contrib import messages
from django.contrib.auth.decorators import login_required
import requests
import json
from django.http import JsonResponse
from rest_framework.authtoken.models import Token
from rest_framework import status
import io
from django.http import FileResponse
from reportlab.lib.pagesizes import letter, landscape
from reportlab.lib import colors

from reportlab.platypus import SimpleDocTemplate, Table, TableStyle


@login_required(login_url="/auth-user/login-user")
def avaliacoesTable(request):
    acao_id = request.GET.get("acao_id")
    avaliacoes = Avaliacao.objects
    if acao_id:
        avaliacoes = avaliacoes.filter(acao__id=acao_id)

    avaliacoes = avaliacoes.all()
    print(avaliacoes)
    return render(
        request, "avaliacoes/avaliacoes_table.html", {"avaliacoes": avaliacoes}
    )


@login_required(login_url="/auth-user/login-user")
def avaliacoesDpEventoTable(request):
    evento_id = request.GET.get("dp_evento_id")
    avaliacoes = Avaliacao.objects
    if evento_id:
        avaliacoes = avaliacoes.filter(evento__id=evento_id)
    avaliacoes = avaliacoes.all()
    print(avaliacoes)
    return render(
        request, "avaliacoes/avaliacoes_table.html", {"avaliacoes": avaliacoes}
    )


@login_required(login_url="/auth-user/login-user")
def eliminarAvaliacao(request, id):
    avaliacao = Avaliacao.objects.get(id=id)
    avaliacao.delete()
    messages.success(request, "Avaliação eliminada com sucesso!")
    return JsonResponse({"message": "Deletado com sucesso"}, status=status.HTTP_200_OK)


@login_required(login_url="/auth-user/login-user")
def avaliacaoModal(request):
    acao_id = request.GET.get("acao_id")
    evento_id = request.GET.get("dp_evento_id")
    title = request.GET.get("title")
    modalId = request.GET.get("modalId")
    avaliacao_id = request.GET.get("avaliacao_id")
    print(modalId)
    data = {}
    if acao_id:
        acao = Acao.objects.get(id=acao_id)
        data["acao"] = acao
    if evento_id:
        evento = DpEvento.objects.get(id=evento_id)
        data["evento"] = evento
    if modalId:
        data["modalId"] = modalId
    if avaliacao_id:
        avaliacao = Avaliacao.objects.get(id=avaliacao_id)
        data["avaliacao"] = avaliacao
    data["title"] = title
    return render(request, "avaliacoes/avaliacaoModal.html", data)


@login_required(login_url="/auth-user/login-user")
def saveAvaliacao(request):
    token, created = Token.objects.get_or_create(user=request.user)
    headers = {"Authorization": "Token " + token.key}
    body = json.loads(request.body)["data"]
    response = requests.post(
        "http://localhost:8000/avaliacoes", json=body, headers=headers
    )
    return JsonResponse(json.loads(response.content), status=response.status_code)


@login_required(login_url="/auth-user/login-user")
def updateAvaliacao(request, id):
    token, created = Token.objects.get_or_create(user=request.user)
    headers = {"Authorization": "Token " + token.key}
    body = json.loads(request.body)["data"]
    print("dados para update avaliacao", body)
    response = requests.put(
        "http://localhost:8000/avaliacoes/" + str(id), json=body, headers=headers
    )
    return JsonResponse(json.loads(response.content), status=response.status_code)


@login_required(login_url="/auth-user/login-user")
def updateAvaliacao(request, id):
    token, created = Token.objects.get_or_create(user=request.user)
    headers = {"Authorization": "Token " + token.key}
    body = json.loads(request.body)["data"]
    print("dados para update avaliacao", body)
    response = requests.put(
        "http://localhost:8000/avaliacoes/" + str(id), json=body, headers=headers
    )
    return JsonResponse(json.loads(response.content), status=response.status_code)

@login_required(login_url="/auth-user/login-user")
def avaliacaoRelatorio(request, id):
    # Fetch data from Avaliacao model
    avaliacoes = Avaliacao.objects.all()

    # Create a file-like buffer to receive PDF data
    buffer = io.BytesIO()

    # Set up the PDF document
    doc = SimpleDocTemplate(buffer, pagesize=landscape(letter))

    # Build the table data
    data = [
        ["Campo", "Valor"]
    ]  # Add table header
    for avaliacao in avaliacoes:
        data.append(
            [
                avaliacao.id,
                avaliacao.observacaoGeral,  # Replace 'field1' with the actual field name
                avaliacao.salaCulinariaObservacao,
                avaliacao.salaServicosBelezaObservacao,  # Replace 'field3' with the actual field name
            ]
        )

    # Create the table
    table = Table(data)
    table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), colors.grey),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
                ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                ("FONTSIZE", (0, 0), (-1, 0), 14),
                ("BOTTOMPADDING", (0, 0), (-1, 0), 12),
                ("BACKGROUND", (0, 1), (-1, -1), colors.beige),
                ("GRID", (0, 0), (-1, -1), 1, colors.black),
            ]
        )
    )

    # Add the table to the PDF document
    doc.build([table])

    # Get the value of the BytesIO buffer and write it to the response
    buffer.seek(0)
    pdf = buffer.getvalue()
    buffer.close()

    # Send the response with the PDF file
    response = FileResponse(io.BytesIO(pdf), content_type="application/pdf")
    response["Content-Disposition"] = 'inline; filename="avaliacao-relatorio.pdf"'

    return response
