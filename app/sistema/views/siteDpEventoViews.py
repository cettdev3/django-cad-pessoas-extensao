from django.shortcuts import render, redirect
from sistema.models.dpEvento import DpEvento
from sistema.models.membroExecucao import MembroExecucao
from sistema.models.escola import Escola
from sistema.models.ensino import Ensino
from sistema.models.tipoAtividade import TipoAtividade
from sistema.models.atividade import Atividade
from sistema.services.camunda import CamundaAPI
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Q
import itertools
import requests
from docx.enum.text import WD_UNDERLINE
from docx.shared import Pt, RGBColor
import json
import os
from django.http import HttpResponse
from django.http import FileResponse
import docx
from django.http import JsonResponse
from rest_framework.authtoken.models import Token
from sistema.serializers.dpEventoSerializer import DpEventoSerializer
from sistema.serializers.ensinoSerializer import EnsinoSerializer
from sistema.serializers.escolaSerializer import EscolaSerializer
from django.db.models import Prefetch
from collections import defaultdict

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
    print("dentro de visualizarDpEvento")
    dpEvento = DpEvento.objects.prefetch_related(
        Prefetch(
            "membroexecucao_set", 
            queryset=MembroExecucao.objects
            .select_related("itinerario")
            .prefetch_related("ticket_set")
            .prefetch_related("itinerario__itinerarioitem_set")
        ),
    ).get(id=codigo)
    page_title = dpEvento.tipo_formatado+" - "+dpEvento.cidade.nome
    path_back = "gerencia_dp_eventos"
    dpEvento = DpEventoSerializer(dpEvento).data

    return render(request,'dpEventos/visualizar_dp_evento.html',{
        'dpEvento':dpEvento, 
        'page_title': page_title,
        'path_back': path_back
    })

def createRelatorioGPS(doc, counter, filters):
    eventos = None
    print("filtros", filters)
    if 'departamento_id' in filters and filters['departamento_id']:
        eventos = DpEvento.objects.prefetch_related(
        Prefetch(
            'atividade_set',
            queryset=Atividade.objects.select_related(
                'tipoAtividade'
            ).filter(departamento=filters['departamento_id'])
        )).filter(tipo=DpEvento.CURSO_GPS)
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

    for key,tipoEvento in result.items():
        title = doc.add_paragraph()
        title_run = title.add_run(f'{key}')
        title_run.bold = True
        title_run.underline = WD_UNDERLINE.SINGLE
        title.space_after = Pt(0)

        for skey, values in tipoEvento.items():
            title_run = doc.add_paragraph()
            title_run = title_run.add_run(f'{skey}')
            title_run.bold = True
            title_run.underline = WD_UNDERLINE.SINGLE
            title_run.space_after = Pt(0)
            
            atividades = values
            if len(atividades) == 0 or not atividades[0].tipoAtividade:
                continue
            
            tipoAtividadeDescricao = doc.add_paragraph()
            tipoAtividadeDescricao = tipoAtividadeDescricao.add_run(f'{atividades[0].tipoAtividade.descricao}')

            for atividade in atividades:
                acaoCargaHoraria = ""
                cidade = ""
                matriculas = ""
                alunosCertificados = ""
                dataInicio = ""
                dataFim = ""
                local = ""
                etapa = ""
                cursos = []
                acaoCargaHoraria = f"Ação {str(counter)}: {int(atividade.cargaHoraria)}h"
                cidade = f"{atividade.cidade.nome}"
                if atividade.quantidadeMatriculas:
                    matriculas = f"{atividade.quantidadeMatriculas}"
                if atividade.quantidadeCertificacoes:
                    alunosCertificados = f"{atividade.quantidadeCertificacoes}"
                evento = atividade.evento
                dataInicio = f"{evento.data_inicio.strftime('%d/%m/%Y')}" 
                dataFim = f"{evento.data_fim.strftime('%d/%m/%Y')}"
                local = f"{atividade.endereco_completo}"
                if evento.acaoEnsino:
                    etapa = f"{evento.acaoEnsino.observacao}"
                    alocacoes = evento.acaoEnsino.alocacao_set.all()
                    if alocacoes:
                        for alocacao in alocacoes:
                            cursos.append(f"{alocacao.curso.nome}")

                section_title = doc.add_paragraph()
                section_title_run = section_title.add_run(f'{acaoCargaHoraria}')
                section_title_run.bold = True
                section_title_run.underline = WD_UNDERLINE.SINGLE
                section_title_format = section_title.paragraph_format
                section_title_format.space_after = Pt(0)

                cidadeParagraph = doc.add_paragraph()
                cidadeParagraph.add_run(f"cidade:").bold = True
                cidadeParagraph.add_run(f" {cidade}")
                cidadeParagraphFormat = cidadeParagraph.paragraph_format
                cidadeParagraphFormat.space_after = Pt(0)
                
                if matriculas:
                    matriculasParagraph = doc.add_paragraph()
                    matriculasParagraph.add_run(f"Matriculas:").bold = True
                    matriculasParagraph.add_run(f" {matriculas}")
                    matriculasParagraphFormat = matriculasParagraph.paragraph_format
                    matriculasParagraphFormat.space_after = Pt(0)

                dataParagraph = doc.add_paragraph()
                dataParagraph.add_run(f"data:").bold = True
                dataParagraph.add_run(f" {dataInicio} até {dataFim}")
                dataParagraphFormat = dataParagraph.paragraph_format
                dataParagraphFormat.space_after = Pt(0)

                localParagraph = doc.add_paragraph()
                localParagraph.add_run(f"local:").bold = True
                localParagraph.add_run(f" {local}")
                localParagraphFormat = localParagraph.paragraph_format
                localParagraphFormat.space_after = Pt(0)

                etapaParagraph = doc.add_paragraph()
                etapaParagraph.add_run(f"etapa:").bold = True
                etapaParagraph.add_run(f" {etapa}")
                etapaParagraphFormat = etapaParagraph.paragraph_format
                etapaParagraphFormat.space_after = Pt(0)

                cursosParagraph = doc.add_paragraph()
                cursosParagraph.add_run(f"Cursos oferecidos:").bold = True
                cursosParagraphFormat = cursosParagraph.paragraph_format
                cursosParagraphFormat.space_after = Pt(0)
                
                for curso in cursos:
                    cursoParagraph = doc.add_paragraph(f"{curso};")
                    cursoParagraphFormat = cursoParagraph.paragraph_format
                    cursoParagraphFormat.space_after = Pt(0)

                if alunosCertificados:
                    etapaParagraph = doc.add_paragraph()
                    etapaParagraph.add_run(f"Alunos certificados:").bold = True
                    etapaParagraph.add_run(f" {alunosCertificados}")
                    etapaParagraphFormat = etapaParagraph.paragraph_format
                    etapaParagraphFormat.space_after = Pt(0)
                doc.add_paragraph()
                counter += 1
                
    return doc, counter

def createRelatorioOutros(doc, counter, filters):
    eventos = None
    if 'departamento_id' in filters  and filters['departamento_id']:
        eventos = DpEvento.objects.prefetch_related(
        Prefetch(
            'atividade_set',
            queryset=Atividade.objects.select_related(
                'tipoAtividade'
            ).filter(
                departamento=filters['departamento_id']
            )
        )).filter(~Q(tipo=DpEvento.CURSO_GPS))
    else:
        eventos = DpEvento.objects.prefetch_related(
        Prefetch(
            'atividade_set',
            queryset=Atividade.objects.select_related(
                'tipoAtividade'
            )
        )).filter(~Q(tipo=DpEvento.CURSO_GPS))
    
    if 'data_inicio' in filters:
        eventos = eventos.filter(data_inicio__gte=filters['data_inicio'])
    if 'data_fim' in filters:
        eventos = eventos.filter(data_fim__lte=filters['data_fim'])

    atividadesCounter = counter
    for evento in eventos:
        # if evento has no activities, skip it
        if not evento.atividade_set.all():
            continue
        title = doc.add_paragraph()
        title_run = title.add_run(f'{evento.tipo_formatado} - {evento.cidade.nome}')
        title_run.bold = True
        title_run.underline = WD_UNDERLINE.SINGLE
        title.space_after = Pt(0)

        atividades = evento.atividade_set.all()
        for atividade in atividades:
            if not atividade.tipoAtividade:
                continue
            if atividade.cargaHoraria is None:
                continue
            
            tipo = atividade.tipoAtividade.nome
            print("atividadesCounter", atividadesCounter)
            acaoCargaHoraria = f"Ação {atividadesCounter} - {str(int(atividade.cargaHoraria))}h"

            service_cargaHoraria_title = doc.add_paragraph()
            service_cargaHoraria_title_run = service_cargaHoraria_title.add_run(f'{acaoCargaHoraria}')
            service_cargaHoraria_title_run.bold = True
            service_cargaHoraria_title_run.underline = WD_UNDERLINE.SINGLE
            service_cargaHoraria_title_format = service_cargaHoraria_title.paragraph_format
            service_cargaHoraria_title_format.space_after = Pt(0)
            
            cidade = f"{atividade.cidade.nome}"
            cidadeParagraph = doc.add_paragraph()
            cidadeParagraph.add_run(f"cidade: ").bold = True
            cidadeParagraph.add_run(f" {cidade}")
            cidadeParagraphFormat = cidadeParagraph.paragraph_format
            cidadeParagraphFormat.space_after = Pt(0)

            dataInicio = f"{evento.data_inicio.strftime('%d/%m/%Y')}"
            dataFim = f"{evento.data_fim.strftime('%d/%m/%Y')}"
            dataParagraph = doc.add_paragraph()
            dataParagraph.add_run(f"data: ").bold = True
            dataParagraph.add_run(f" {dataInicio} até {dataFim}")
            dataParagraphFormat = dataParagraph.paragraph_format
            dataParagraphFormat.space_after = Pt(0)

            local = f"{evento.escola.nome}"
            localParagraph = doc.add_paragraph()
            localParagraph.add_run(f"local: ").bold = True
            localParagraph.add_run(f" {local}")
            localParagraphFormat = localParagraph.paragraph_format
            localParagraphFormat.space_after = Pt(0)
            
            if not atividade.quantidadeCertificacoes:
                servicosParagraph = doc.add_paragraph()
                servicosParagraph.add_run(f"Serviços oferecidos: ").bold = True
                servicosParagraphFormat = servicosParagraph.paragraph_format
                servicosParagraphFormat.space_after = Pt(0)

                servicos = atividade.tipoAtividade.nome
                if servicos == "serviços diversos":
                    servicos_set = atividade.servico_set.all()
                    servicos = ""
                    for servico in servicos_set:
                        servicoOferecidoParagraph = doc.add_paragraph()
                        servicoOferecidoParagraph.add_run(f" - {servico.nome}")
                        servicoOferecidoParagraphFormat = servicoOferecidoParagraph.paragraph_format
                        servicoOferecidoParagraphFormat.space_after = Pt(0)
                else:
                    servicoOferecidoParagraph = doc.add_paragraph()
                    servicoOferecidoParagraph.add_run(f" - {atividade.tipoAtividade.nome}")
                    servicoOferecidoParagraphFormat = servicoOferecidoParagraph.paragraph_format
                    servicoOferecidoParagraphFormat.space_after = Pt(0)
                
                servicos = atividade.tipoAtividade.nome
                if servicos == "serviços diversos":
                    servicos_set = atividade.servico_set.all()
                    servicos = ""
                    
                    vendasParagraph = doc.add_paragraph()
                    vendasParagraph.add_run(f"Número de vendas: ").bold = True
                    vendasParagraphFormat = vendasParagraph.paragraph_format
                    vendasParagraphFormat.space_after = Pt(0)

                    for servico in servicos_set:
                        servicoOferecidoParagraph = doc.add_paragraph()
                        servicoOferecidoParagraph.add_run(f" - {servico.nome}: {str(int(servico.quantidadeVendas))} vendas")
                        servicoOferecidoParagraphFormat = servicoOferecidoParagraph.paragraph_format
                        servicoOferecidoParagraphFormat.space_after = Pt(0)

                servicos = atividade.tipoAtividade.nome
                qtdAtendimentos = atividade.quantidadeAtendimentos
                if servicos == "serviços diversos":
                    servicos_set = atividade.servico_set.all()
                    servicos = ""
                    servicosAtendimentosCounter = 0
                    for servico in servicos_set:
                        servicosAtendimentosCounter += servico.quantidadeAtendimentos if servico.quantidadeAtendimentos else 0
                    qtdAtendimentos = atividade.quantidadeAtendimentos if atividade.quantidadeAtendimentos else servicosAtendimentosCounter
                if qtdAtendimentos:
                    pessoasAtendidasParagraph = doc.add_paragraph()
                    pessoasAtendidasParagraph.add_run(f"Quantidade de Atendimentos: ").bold = True
                    pessoasAtendidasParagraph.add_run(f" {qtdAtendimentos}")
                    pessoasAtendidasParagraphFormat = pessoasAtendidasParagraph.paragraph_format
                    pessoasAtendidasParagraphFormat.space_after = Pt(0)

            if atividade.quantidadeCertificacoes:
                quantidadeCertificacoes = f"{str(int(atividade.quantidadeCertificacoes))}"
                quantidadeCertificacoesParagraph = doc.add_paragraph()
                quantidadeCertificacoesParagraph.add_run(f"Quantidade de certificações: ").bold = True
                quantidadeCertificacoesParagraph.add_run(f" {quantidadeCertificacoes}")
                quantidadeCertificacoesParagraphFormat = quantidadeCertificacoesParagraph.paragraph_format
                quantidadeCertificacoesParagraphFormat.space_after = Pt(0)
            
            if atividade.quantidadeMatriculas:
                quantidadeMatriculas = f"{str(int(atividade.quantidadeMatriculas))}"
                quantidadeMatriculasParagraph = doc.add_paragraph()
                quantidadeMatriculasParagraph.add_run(f"Quantidade de matrículas: ").bold = True
                quantidadeMatriculasParagraph.add_run(f" {quantidadeMatriculas}")
                quantidadeMatriculasParagraphFormat = quantidadeMatriculasParagraph.paragraph_format
                quantidadeMatriculasParagraphFormat.space_after = Pt(0)

            if atividade.quantidadeInscricoes:
                quantidadeInscricoes = f"{str(int(atividade.quantidadeInscricoes))}"
                quantidadeInscricoesParagraph = doc.add_paragraph()
                quantidadeInscricoesParagraph.add_run(f"Quantidade de inscrições: ").bold = True
                quantidadeInscricoesParagraph.add_run(f" {quantidadeInscricoes}")
                quantidadeInscricoesParagraphFormat = quantidadeInscricoesParagraph.paragraph_format
                quantidadeInscricoesParagraphFormat.space_after = Pt(0)

            doc.add_paragraph()
            atividadesCounter += 1

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

    counter = int(1)
    doc, counter = createRelatorioGPS(doc, counter, filters)
    doc = createRelatorioOutros(doc, counter, filters)
    with open('dp_evento_report.docx', 'wb') as f:
        doc.save(f)

    response = FileResponse(open('dp_evento_report.docx', 'rb'))
    response['Content-Type'] = 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'
    response['Content-Disposition'] = 'attachment; filename="dp_evento_report.docx"'

    os.remove('dp_evento_report.docx')
    return response