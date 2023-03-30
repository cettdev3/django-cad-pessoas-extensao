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
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.units import inch
from reportlab.lib.enums import TA_CENTER




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

def createTableHeader(title):
    header_style = ParagraphStyle(
        name='header',
        alignment=TA_CENTER,
        textColor=colors.white,
    )

    header_row = [Paragraph(f'<b>{title}</b>', header_style), '']
    header_data = [header_row]
    return header_data

def createTable(header_data, attributes, available_width):
    table_data = header_data + [[desc, value] for desc, value in attributes]
    table = Table(table_data, colWidths=[available_width * 0.3, available_width * 0.7])

    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('SPAN', (0, 0), (-1, 0)),
        ('ALIGN', (0, 0), (0, -1), 'LEFT'),
        ('ALIGN', (1, 0), (1, -1), 'RIGHT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 14),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 1), (-1, -1), 12),
        ('LINEBELOW', (0, 0), (-1, -1), 1, colors.black),  # Add border line below all cells
    ]))
    return table

def createParagraph(description):
    styles = getSampleStyleSheet()
    paragraph = Paragraph(f"<b>Observação: </b> {description}", styles['Normal'])
    return paragraph

def createHeader(endereco, evento_tipo, evento_data_inicio, evento_data_fim, avaliador):
    styles = getSampleStyleSheet()
    header = Paragraph(
        f"<b>Endereço: </b> {endereco} <br/> <b>Tipo de evento: </b> {evento_tipo} <br/> <b>Data de início: </b> {evento_data_inicio} <br/> <b>Data de fim: </b> {evento_data_fim} <br/> <b>Avaliador: </b> {avaliador}",
        styles['Normal'],
    )
    return header

@login_required(login_url="/auth-user/login-user")
def avaliacaoRelatorio(request, id):
    avaliacao = Avaliacao.objects.get(id=id)

    # Create the PDF object
    pdf_buffer = io.BytesIO()
    pdf_document = SimpleDocTemplate(
        pdf_buffer,
        pagesize=letter,
        leftMargin=28.346 * 2,
        rightMargin=28.346 * 2,
        topMargin=28.346 * 2,
        bottomMargin=28.346 * 2,
    )

    page_width, _ = letter
    available_width = page_width - 28.346 * 4  

    avaliacao_dict = vars(avaliacao)
    description = Avaliacao.atributes_description

    attributesGeral = []
    attributesCulinaria = []
    attributesBeleza = []
    for attr, value in avaliacao_dict.items():
        if not attr.startswith('_') and 'updatedat' not in attr.lower() and 'observacao' not in attr.lower():
            if value is None:
                value = ''
            if attr in description:
                print(f"atributo: {attr}")
                if 'geral' in attr.lower() or 'qtdSalas' == attr:
                    print(f"atributo em geral: {attr}")
                    attributesGeral.append((description[attr], value))
                elif 'culinaria' in attr.lower():
                    attributesCulinaria.append((description[attr], value))
                elif 'beleza' in attr.lower():
                    attributesBeleza.append((description[attr], value))

    # table geral
    header_data_geral = createTableHeader("Dados Gerais do Local")
    tableGeral = createTable(header_data_geral, attributesGeral, available_width)
    paragraph = createParagraph(avaliacao.observacaoGeral)

    # table culinaria
    header_data_culinaria = createTableHeader("Dados da Sala de Cursos de Culinária")
    tableCulinaria = createTable(header_data_culinaria, attributesCulinaria, available_width)
    paragraphCulinaria = createParagraph(avaliacao.salaCulinariaObservacao)

    # table beleza
    header_data_beleza = createTableHeader("Dados da Sala de Serviços de Beleza")
    tableBeleza = createTable(header_data_beleza, attributesBeleza, available_width)
    paragraphBeleza = createParagraph(avaliacao.salaServicosBelezaObservacao)

    space = Spacer(1, 0.25*inch)
    header = createHeader(
        avaliacao.endereco_completo, 
        avaliacao.evento.tipo, 
        avaliacao.evento.data_inicio_formatada, 
        avaliacao.evento.data_fim_formatada,
        avaliacao.avaliador.pessoa.nome
    )

    pdf_document.build([
        header,
        space,
        tableGeral, 
        space, 
        paragraph, 
        space, 
        tableCulinaria, 
        space, 
        paragraphCulinaria, 
        space, 
        tableBeleza, 
        space, 
        paragraphBeleza
    ])

    pdf_buffer.seek(0)
    pdf = pdf_buffer.getvalue()
    pdf_buffer.close()

    response = FileResponse(io.BytesIO(pdf), content_type="application/pdf")
    response["Content-Disposition"] = 'inline; filename="avaliacao-relatorio.pdf"'

    return response
