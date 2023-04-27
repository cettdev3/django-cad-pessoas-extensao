from django.shortcuts import render, redirect
from sistema.models.dpEvento import DpEvento
from sistema.models.membroExecucao import MembroExecucao
from sistema.models.escola import Escola
from sistema.models.ensino import Ensino
from sistema.models.tipoAtividade import TipoAtividade
from sistema.services.alfrescoApi import AlfrescoAPI
from sistema.models.atividade import Atividade
from sistema.models.alocacao import Alocacao
from sistema.services.camunda import CamundaAPI
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Q
from PIL import Image
import requests
from docx.enum.text import WD_UNDERLINE, WD_ALIGN_PARAGRAPH
from docx.shared import Pt, Inches
import json
import os
from django.http import FileResponse
import docx
from django.http import JsonResponse
from rest_framework.authtoken.models import Token
from sistema.serializers.dpEventoSerializer import DpEventoSerializer
from sistema.serializers.ensinoSerializer import EnsinoSerializer
from sistema.serializers.escolaSerializer import EscolaSerializer
from django.db.models import Prefetch
from collections import defaultdict
from docx.image.exceptions import UnrecognizedImageError
from docx import Document

@login_required(login_url='/auth-user/login-user')
def gerencia_dp_eventos(request):
    page_title = "Eventos"
    count = 0
    dp_eventos = DpEvento.objects.all()
    for p in dp_eventos:
        count += 1
    
    return render(request,'dpEventos/gerenciar_dp_eventos.html',
    {'dp_eventos':dp_eventos,'contagem':count, "page_title": page_title})

@login_required(login_url='/auth-user/login-user')
def dpEventoTable(request):
    tipo = request.GET.get('tipo')
    data_inicio = request.GET.get('data_inicio')
    data_fim = request.GET.get('data_fim')
    order_by = request.GET.get('order_by')
    token, created = Token.objects.get_or_create(user=request.user)
    headers = {'Authorization': 'Token ' + token.key}

    dpEventoResponse = requests.get('http://localhost:8000/dp-eventos', params={
        'tipo': tipo,
        'data_inicio': data_inicio,
        'data_fim': data_fim,
        'order_by': order_by
    }, headers=headers)
    dpEventoResponseStatusCode = dpEventoResponse.status_code
    dpEventoResponse = json.loads(dpEventoResponse.content.decode())
    
    dpEventos = dpEventoResponse
    return render(request,'dpEventos/dp_eventos_tabela.html',{'dpEventos':dpEventos})

@login_required(login_url='/auth-user/login-user')
def dpEventoModal(request):
    id = request.GET.get('id')
    dpEvento = None
    data = {}
    escolas = Escola.objects.all()
    ensinos = Ensino.objects.all()
    data['escolas'] = EscolaSerializer(escolas, many=True).data
    data['ensinos'] = EnsinoSerializer(ensinos, many=True).data
    data['ct_emprestimo'] = DpEvento.EMPRESTIMO
    if id:
        dpEvento = DpEvento.objects.get(id=id)
        data['dpEvento'] = DpEventoSerializer(dpEvento).data 
    return render(request,'dpEventos/dp_eventos_modal.html',data)

@login_required(login_url='/auth-user/login-user')
def eliminarDpEvento(request,codigo):
    token, created = Token.objects.get_or_create(user=request.user)
    headers = {'Authorization': 'Token ' + token.key}
    
    dpEventoResponse = requests.delete('http://localhost:8000/dp-eventos/'+str(codigo), headers=headers)
    dpEventoResponseStatusCode = dpEventoResponse.status_code
    dpEventoResponse = json.loads(dpEventoResponse.content.decode())

    return redirect('/gerencia_dp_eventos')

@login_required(login_url='/auth-user/login-user')
def saveDpEvento(request):
    token, created = Token.objects.get_or_create(user=request.user)
    headers = {'Authorization': 'Token ' + token.key}
    dpEventoData = json.loads(request.body)['data']
    itinerarios = json.loads(request.body)['itinerarios']
    dpEventoResponse = requests.post(
        'http://localhost:8000/dp-eventos', 
        json={"dpEvento": dpEventoData, "itinerarios": itinerarios}, 
        headers=headers
    )
    dpEventoResponseStatusCode = dpEventoResponse.status_code
    dpEventoResponse = json.loads(dpEventoResponse.content.decode())
    dpEvento = DpEvento.objects.get(id=dpEventoResponse['id'])

    if dpEvento.tipo in DpEvento.MAPPED_TIPOS:
        dados = {
            "variables": {
                "processDescription": {"value": dpEvento.tipo + ", " + dpEvento.cidade.nome, "type": "String"},
                "dpEvento_id": {"value": dpEvento.id, "type": "String"},
                "extrato": {"value": dpEvento.extrato, "type": "String"},
            },
            "withVariablesInReturn": True
        }

        camunda = CamundaAPI()
        camundaResponse = camunda.startProcess("ProcessoDeEmprestimoDeIntensProcess",dados)
        dpEvento.process_instance = camundaResponse['id']
        if dpEvento.tipo == DpEvento.EMPRESTIMO:
            dpEvento.status = DpEvento.STATUS_WAITING_TICKET
        dpEvento.save()

    return JsonResponse(dpEventoResponse, status=dpEventoResponseStatusCode)

@login_required(login_url='/auth-user/login-user')
def editarDpEvento(request, codigo):
    token, created = Token.objects.get_or_create(user=request.user)
    headers = {'Authorization': 'Token ' + token.key}
    body = json.loads(request.body)['data']
    response = requests.put('http://localhost:8000/dp-eventos/'+str(codigo), json=body, headers=headers)
    return JsonResponse(json.loads(response.content),status=response.status_code)

@login_required(login_url='/auth-user/login-user')
def dp_eventosSelect(request):
    dp_eventos = DpEvento.objects.all()
    return render(request,'dpEventos/dp-eventos_select.html',{'dp_eventos':dp_eventos})

@login_required(login_url='/auth-user/login-user')
def visualizarDpEvento(request,codigo):
    print("dentro de visualizarDpEvento", codigo)
    dpEvento = DpEvento.objects.prefetch_related(
        Prefetch(
            "membroexecucao_set", 
            queryset=MembroExecucao.objects
            .select_related("itinerario")
            .prefetch_related("ticket_set")
            .prefetch_related("itinerario__itinerarioitem_set")
        ),
    ).get(id=codigo)

    path_back = "gerencia_dp_eventos"
    dpEvento = DpEventoSerializer(dpEvento).data

    return render(request,'dpEventos/visualizar_dp_evento.html',{
        'dpEvento':dpEvento, 
        'path_back': path_back
    })

def getFilteredEventos(filters):
    eventos = None
    print("filtros", filters)
    if 'departamento_id' in filters and filters['departamento_id']:
        eventos = DpEvento.objects.prefetch_related(
        Prefetch(
            'atividade_set',
            queryset=Atividade.objects.select_related(
                'tipoAtividade'
            ).filter(departamento=filters['departamento_id'])
        ))
    else:
        eventos = DpEvento.objects.prefetch_related(
        Prefetch(
            'atividade_set',
            queryset=Atividade.objects.select_related('tipoAtividade')
        )).filter(tipo=DpEvento.CURSO_GPS)

    if 'data_inicio' in filters:
        eventos = eventos.filter(data_inicio__gte=filters['data_inicio'])
    if 'data_fim' in filters:
        eventos = eventos.filter(data_fim__lte=filters['data_fim'])
    result = {}

    for evento in eventos:
        if evento.atividade_set.count() == 0:
            continue
        tipo = evento.tipo
        result.setdefault(tipo, {})
        
        for atividade in evento.atividade_set.all():
            tipo_atividade = atividade.tipoAtividade.nome
            result[tipo].setdefault(tipo_atividade, [])
            result[tipo][tipo_atividade].append(atividade)

    report = defaultdict(list)
    for dp_evento in eventos:
        report[dp_evento.tipo].append(dp_evento)
    if True:
        return report
    return result

def getSectionTitle(doc, nomeEvento):
    title = doc.add_paragraph()
    title_run = title.add_run(f'{nomeEvento}')
    title_run.bold = True
    title_run.underline = WD_UNDERLINE.SINGLE
    title.space_after = Pt(0)
    return doc

def getCidade(doc, atividade):
    cidade = atividade.cidade
    cidadeParagraph = doc.add_paragraph()
    cidadeParagraph.add_run(f"cidade:").bold = True
    cidadeParagraph.add_run(f" {cidade.nome}")
    cidadeParagraphFormat = cidadeParagraph.paragraph_format
    cidadeParagraphFormat.space_after = Pt(0)
    return doc

def getMatriculas(acaoEnsino):
    alocacoes = acaoEnsino.alocacao_set.all()
    matriculas = 0
    for alocacao in alocacoes:
        matriculas += alocacao.quantidade_matriculas if alocacao.quantidade_matriculas else 0
    return matriculas

def getServicosAtendimentos(atividade):
    servicos = atividade.servico_set.all()
    atendimentos = 0
    for servico in servicos:
        atendimentos += servico.quantidadeAtendimentos if servico.quantidadeAtendimentos else 0
    return atendimentos

def getQuantitativo(doc, atividade):
    quantitativoValor = atividade.tipo_quantitativo_valor
    quantitativoLabel = atividade.tipo_quantitativo_label

    if atividade.evento.acaoEnsino:
        quantitativoValor = getMatriculas(atividade.evento.acaoEnsino)
        quantitativoLabel = 'Quantidade de Matrículas'
    if atividade.servico_set.count() > 0:
        quantitativoValor = getServicosAtendimentos(atividade)

    quantitativoParagraph = doc.add_paragraph()
    quantitativoParagraph.add_run(f"{quantitativoLabel}:").bold = True
    quantitativoParagraph.add_run(f" {quantitativoValor}")
    quantitativoParagraphFormat = quantitativoParagraph.paragraph_format
    quantitativoParagraphFormat.space_after = Pt(0)
    return doc

def getData(doc, atividade):
    dataInicio = atividade.data_realizacao_inicio_formatada
    dataFim = atividade.data_realizacao_fim_formatada
    dataStr = f"{dataInicio} até {dataFim}" if dataInicio != dataFim else f"{dataInicio}"
    dataParagraph = doc.add_paragraph()
    dataParagraph.add_run(f"Data:").bold = True
    dataParagraph.add_run(f" {dataStr}")
    dataParagraphFormat = dataParagraph.paragraph_format
    dataParagraphFormat.space_after = Pt(0)
    return doc

def getLocal(doc, atividade):
    local = atividade.endereco_completo
    localParagraph = doc.add_paragraph()
    localParagraph.add_run(f"Local:").bold = True
    localParagraph.add_run(f" {local}")
    localParagraphFormat = localParagraph.paragraph_format
    localParagraphFormat.space_after = Pt(0)
    return doc

def getEtapa(doc, atividade):
    etapa = atividade.evento.acaoEnsino.etapa_formatada
    if len(etapa) > 0:
        etapaParagraph = doc.add_paragraph()
        etapaParagraph.add_run(f"Etapa:").bold = True
        etapaParagraph.add_run(f" {etapa}")
        etapaParagraphFormat = etapaParagraph.paragraph_format
        etapaParagraphFormat.space_after = Pt(0)
        return doc
    
    return doc

def getSubAtividades(doc: Document, atividade):
    if atividade.evento.acaoEnsino:
        alocacoes = Alocacao.objects.filter(acaoEnsino=atividade.evento.acaoEnsino)
        if alocacoes:
            subAtividadesParagraph = doc.add_paragraph()
            subAtividadesParagraph.add_run(f"Cursos Ofertados:").bold = True
            subAtividadesParagraphFormat = subAtividadesParagraph.paragraph_format
            subAtividadesParagraphFormat.space_after = Pt(0)
            for alocacao in alocacoes:
                curso = alocacao.curso.nome
                codigoSiga = alocacao.codigo_siga if alocacao.codigo_siga else ""
                quantidadeMatriculas = alocacao.quantidade_matriculas if alocacao.quantidade_matriculas else ""
                subAtividadeParagraph = doc.add_paragraph(f"{codigoSiga} {curso}: {quantidadeMatriculas}")
                subAtividadeParagraphFormat = subAtividadeParagraph.paragraph_format
                subAtividadeParagraphFormat.space_after = Pt(0)
            return doc
    if atividade.servico_set.count() > 0:
        subAtividadesParagraph = doc.add_paragraph()
        subAtividadesParagraph.add_run(f"Serviços Ofertados:").bold = True
        subAtividadesParagraphFormat = subAtividadesParagraph.paragraph_format
        subAtividadesParagraphFormat.space_after = Pt(0)
        for servico in atividade.servico_set.all():
            servicoParagraph = doc.add_paragraph(f"{servico.nome}: {servico.quantidadeAtendimentos}")
            servicoParagraphFormat = servicoParagraph.paragraph_format
            servicoParagraphFormat.space_after = Pt(0)
        return doc
    return doc

def getAtividadeLabel(doc, atividade, counter):
    cargaHoraria = atividade.cargaHoraria if atividade.cargaHoraria else ""
    atividadeLabel = doc.add_paragraph()
    atividadeLabel.add_run(f"Ação {counter} - {cargaHoraria}").bold = True
    atividadeLabelFormat = atividadeLabel.paragraph_format
    atividadeLabelFormat.space_after = Pt(0)
    return doc

def getAtividadeImage(doc: Document, atividade, counter):
    # Assuming atividade has an image instance
    imagem = atividade.galeria.imagem_set.first()
    if not imagem:
        return doc
    # Access AlfrescoAPI to get the image content and save it locally
    alfresco_api = AlfrescoAPI()
    image_path = f"tmp/{imagem.id_alfresco}.jpg"
    alfresco_api.getNodeContent(image_path, imagem.id_alfresco)

    # Use Pillow to read and save the image
    try:
        img = Image.open(image_path)
        img.save(image_path)
    except IOError:
        print("Error: Unable to read or save the image using Pillow")

    # Add image description
    p = doc.add_paragraph()
    p.add_run(f"Figura {counter}: {imagem.descricao}")
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER

    # Add the image to the docx
    try:
        img_paragraph = doc.add_paragraph()
        img_run = img_paragraph.add_run()
        img_run.add_picture(image_path, width=Inches(4.0))
        img_paragraph.alignment = WD_ALIGN_PARAGRAPH.CENTER
    except UnrecognizedImageError:
        error_message = f"Error: Unable to recognize the image format for {imagem.descricao}."
        p = doc.add_paragraph()
        p.add_run(error_message)
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    finally:
        # Delete the image file
        try:
            os.remove(image_path)
        except OSError as e:
            print(f"Error: Unable to delete the image file: {e}")

    return doc


def getAtividade(doc, atividade, counter):
    doc = getAtividadeLabel(doc, atividade, counter)
    doc = getCidade(doc, atividade)
    doc = getQuantitativo(doc, atividade)
    doc = getData(doc, atividade)
    doc = getLocal(doc, atividade)
    if atividade.evento.acaoEnsino:
        doc = getEtapa(doc, atividade)
    doc = getSubAtividades(doc, atividade)
    doc.add_paragraph()
    doc = getAtividadeImage(doc, atividade, counter)
    doc.add_paragraph()
    return doc

def getRelatorioType1(doc, relatorioData):
    counter = 0
    for nomeEvento, eventos in relatorioData.items():
        doc = getSectionTitle(doc, nomeEvento)
        old_evento = 0
        for evento in eventos:
            current_evento = evento.id
            for atividade in evento.atividade_set.all():
                if current_evento != old_evento:
                    doc = getSectionTitle(doc, f"{evento.tipo} - {evento.cidade.nome}")
                    old_evento = current_evento

                doc = getSectionTitle(doc, f"{atividade.tipoAtividade.nome}")
                counter = counter + 1
                doc = getAtividade(doc, atividade, counter)
    return doc

def getRelatorioType2(doc, relatorioData):
    for nomeEvento, tiposAtividades in relatorioData.items():
        print("nomeEvento", nomeEvento)
        doc = getSectionTitle(doc, nomeEvento)
        for index, (nomeAtividade, atividades) in enumerate(tiposAtividades.items()):
            if index == 0:
                print("primeiro index")
                
            print("nomeAtividade", nomeAtividade)
            for atividade in atividades:
                print("atividade individual", atividade)

    return doc

def createRelatorio(doc, relatorioData, type = "type 1"):
    if type == "type 1":
        return getRelatorioType1(doc, relatorioData)
    if type == "type 2":
        return getRelatorioType2(doc, relatorioData)
    return doc

@login_required(login_url='/auth-user/login-user')
def relatorioDpEvento(request):
    filters = {}
    if request.GET.get('departamento_id'):
        filters['departamento_id'] = request.GET.get('departamento_id')
    if request.GET.get('data_inicio'):
        filters['data_inicio'] = request.GET.get('data_inicio')
    if request.GET.get('data_fim'):
        filters['data_fim'] = request.GET.get('data_fim')

    doc = docx.Document()
    relatorioData = getFilteredEventos(filters)
    doc = createRelatorio(doc, relatorioData)
    with open('dp_evento_report.docx', 'wb') as f:
        doc.save(f)

    response = FileResponse(open('dp_evento_report.docx', 'rb'))
    response['Content-Type'] = 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'
    response['Content-Disposition'] = 'attachment; filename="dp_evento_report.docx"'

    os.remove('dp_evento_report.docx')
    return response