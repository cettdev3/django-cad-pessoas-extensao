from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
import requests
import json
from itertools import chain
from django.http import HttpResponse, JsonResponse
from rest_framework.authtoken.models import Token
from sistema.models.ticket import Ticket
from sistema.models.escola import Escola
from sistema.models.pessoa import Pessoas
from sistema.models.ensino import Ensino
from sistema.models.membroExecucao import MembroExecucao
from sistema.models.atividade import Atividade
from sistema.models.alocacao import Alocacao
import xlsxwriter
import pandas as pd
import io
from django.core.files.uploadedfile import InMemoryUploadedFile
from io import BytesIO
from fuzzywuzzy import process, fuzz

@login_required(login_url='/auth-user/login-user')
def gerencia_demandas(request):
    page_title = "Demandas"
    return render(request,'demandas/gerenciar_demandas.html',
    {"page_title": page_title})


@login_required(login_url='/auth-user/login-user')
def demandas_tabela(request):
    token, created = Token.objects.get_or_create(user=request.user)
    headers = {'Authorization': 'Token ' + token.key}
    status = request.GET.get('status')
    favorecido = request.GET.get('favorecido')
    escola = request.GET.get('escola')
    order_by = request.GET.get('order_by')

    response = requests.get('http://localhost:8000/tickets', 
    headers=headers, params={
        'status':status,
        'favorecido':favorecido,
        'escola':escola,
        'order_by':order_by
    })
    demandas = json.loads(response.content)
    return render(request,'demandas/demandas_tabela.html',
    {'demandas':demandas})
@login_required(login_url='/auth-user/login-user')
def saveBatchDemanda(request):
    if request.method == 'POST':
        token, created = Token.objects.get_or_create(user=request.user)
        headers = {'Authorization': 'Token ' + token.key}
        demandas = json.loads(request.body)
        extrato = []
        for demanda in demandas:
            response = requests.post('http://localhost:8000/tickets',headers=headers, data=demanda)
            if response.status_code != 201 and response.status_code != 200:
                message = json.loads(response.content)['res']
                linha = demanda["row"]
                extrato.append({"status": "Erro", "linha":linha,"message":message})
            else:
                extrato.append({"status": "Sucesso", "linha":demanda["row"],"message":"Demanda cadastrada com sucesso"})
        return render(request,'demandas/demandas_extrato_importacao.html', {'extrato': extrato})
    else:
        return JsonResponse({'error': 'Invalid POST request'})

@login_required(login_url='/auth-user/login-user')
def demandasSelect(request):
    demandas = None
    evento_id = request.GET.get('evento_id')
    atividade_id = request.GET.get('atividade_id')
    if evento_id:
        membro_execucao_objs = MembroExecucao.objects.filter(evento__id=evento_id)
        ensino_objs = Ensino.objects.filter(dpevento__id=evento_id)
        alocacao_objs = Alocacao.objects.filter(acaoEnsino__in=ensino_objs)
        atividade_objs = Atividade.objects.filter(evento__id=evento_id)

        tickets_membro_execucao = Ticket.objects.filter(membro_execucao__in=membro_execucao_objs)
        tickets_alocacao = Ticket.objects.filter(alocacao__in=alocacao_objs)
        tickets_atividade = Ticket.objects.filter(atividade__in=atividade_objs)

        demandas = list(chain(tickets_membro_execucao, tickets_alocacao, tickets_atividade))

    demandasFiltradas = []
    if atividade_id:
        for ticket in demandas:
            if not ticket.atividade:
                demandasFiltradas.append(ticket)
            elif ticket.atividade.id != int(atividade_id):
                demandasFiltradas.append(ticket)

    return render(request,'demandas/demandas_select.html',
    {'demandas':demandasFiltradas})

@login_required(login_url='/auth-user/login-user')
def relatorio_sintetico(request):
    output = BytesIO()
    workbook = xlsxwriter.Workbook(output)
    worksheet = workbook.add_worksheet()

    centered = workbook.add_format()
    centered.set_align('center')
    centered.set_align('vcenter')
    centered.set_text_wrap(True)
    headers = [
        "Ação/Evento",
        "ID Protocolo",
        "Descrição",
        "Valor Previsto",
        "Valor Executado",
        "COTEC Responsável",
    ]

    max_len_headers = [len(header) for header in headers]

    worksheet.write(0, headers.index("Ação/Evento"), "Ação/Evento", centered)
    worksheet.write(0, headers.index("ID Protocolo"), "ID Protocolo", centered)
    worksheet.write(0, headers.index("Descrição"), "Descrição", centered)
    worksheet.write(0, headers.index("Valor Previsto"), "Valor Previsto", centered)
    worksheet.write(0, headers.index("Valor Executado"), "Valor Executado", centered)
    worksheet.write(0, headers.index("COTEC Responsável"), "COTEC Responsável", centered)
    
    tickets = Ticket.objects.all()

    for i, header in enumerate(headers):
        worksheet.set_column(i, i, max_len_headers[i])

    workbook.close()

    response = HttpResponse(output.getvalue(), content_type="application/vnd.ms-excel")
    response["Content-Disposition"] = "attachment; filename=RelatorioSintetico.xlsx"
    return response

@login_required(login_url='/auth-user/login-user')
def importDemandaModal(request):
    if request.method == 'POST':
        file_obj = request.FILES.get('file')
        if file_obj is not None:
            if isinstance(file_obj, InMemoryUploadedFile):
                excel_file = io.BytesIO(file_obj.read())
            else:
                excel_file = file_obj.temporary_file_path()
            df = pd.read_excel(excel_file)
            df['Data Inicio'] = pd.to_numeric(df['Data Inicio'], errors='coerce')
            df['Data Inicio'] = pd.to_datetime(df['Data Inicio'], errors='coerce', origin='1899-12-30', unit='D')
            df['Data Fim'] = pd.to_numeric(df['Data Fim'], errors='coerce')
            df['Data Fim'] = pd.to_datetime(df['Data Fim'], errors='coerce', origin='1899-12-30', unit='D')
            df['Data Inicio'] = pd.to_datetime(df['Data Inicio'], unit='ms')
            df['Data Inicio'] = df['Data Inicio'].dt.strftime('%Y-%m-%d')
            df['Data Fim'] = pd.to_datetime(df['Data Fim'], unit='ms')
            df['Data Fim'] = df['Data Fim'].dt.strftime('%Y-%m-%d')

            df.reset_index(inplace=True)
            json_data = df.to_json(orient='records')
            data = json.loads(json_data)
            data_to_import = []
            table_data = []

            escolas = list(Escola.objects.all().values_list('id', 'nome'))
            escola_dict = {nome: id for id, nome in escolas}
            pessoas = list(Pessoas.objects.all().values_list('id', 'nome'))
            pessoa_dict = {nome: id for id, nome in pessoas}
            for record in data:
                record_evento_id = record['ID Evento']
                record_id_protocolo = record['ID Protocolo']
                record_escola = record['Departamento']
                record_tipo = record['Tipo']
                record_descricao = record.get('Assunto (Descrição do ID)') or ''
                record_motivo = record.get('Descrição (Motivo da Solicitação)') or ''
                record_data_inicio = record['Data Inicio']
                record_data_fim = record['Data Fim']
                record_status = record['Status']
                record_valor_orcado = record.get('Valor Previsto')
                record_valor_executado = record['Valor Utilizado']
                record_beneficiario = record['Beneficiário']
                record_model = "beneficiario"
                record_rubrica = record['rubrica (1 - , 6 - extensão)']
                rowNumber = record['index'] + 2
                record_membro_execucao = None
                record_alocacao = None
                record_pessoa = None
                record_atividade = None
                record_meta = None
                record_nao_se_aplica_data_inicio = None
                record_nao_se_aplica_data_fim = None
                record_bairro = None
                record_logradouro = None
                record_cep = None
                record_complemento = None
                record_cidade = None

                row_data = {
                    "record_escola": record_escola,
                    "record_tipo": record_tipo,
                    "record_status": record_status,
                    "record_evento_id": record_evento_id,
                    "record_id_protocolo": record_id_protocolo,
                    "record_membro_execucao": record_membro_execucao,
                    "record_alocacao": record_alocacao,
                    "record_pessoa": record_pessoa,
                    "record_atividade": record_atividade,
                    "record_rubrica": record_rubrica,
                    "record_model": record_model,
                    "record_meta": record_meta,
                    "record_data_inicio": record_data_inicio,
                    "record_data_fim": record_data_fim,
                    "record_nao_se_aplica_data_inicio": record_nao_se_aplica_data_inicio,
                    "record_nao_se_aplica_data_fim": record_nao_se_aplica_data_fim,
                    "record_bairro": record_bairro,
                    "record_logradouro": record_logradouro,
                    "record_cep": record_cep,
                    "record_complemento": record_complemento,
                    "record_cidade": record_cidade,
                    "record_descricao": record_descricao,
                    "record_motivo": record_motivo,
                    "record_valor_orcado": record_valor_orcado,
                    "record_valor_executado": record_valor_executado,
                    "record_beneficiario": record_beneficiario,
                    "rowNumber": rowNumber,
                }

                importData = {
                    "tipo": record_tipo,
                    "data_inicio": record_data_inicio or None,
                    "data_fim": record_data_fim or None,
                    "id_protocolo": record_id_protocolo,
                    "status": "CRIADO" ,
                    "valor_orcado": record_valor_orcado,
                    "valor_executado": record_valor_executado,
                    "evento_id": record_evento_id,
                    "beneficiario": record_beneficiario,
                    "escola": record_escola,
                    "observacao": record_descricao + ". "+ record_motivo,
                    "model": record_model,
                    "rubrica": record_rubrica,
                    "from_export": True,
                    "rowNumber": rowNumber,
                    "membro_execucao": None,
                    "atividade": None,
                    "alocacao": None,
                    "pessoa": None,
                    "servico_contratado": None,
                    "meta": None,
                    "nao_se_aplica_data_inicio": None,
                    "nao_se_aplica_data_fim": None,
                    "bairro": None,
                    "logradouro": None,
                    "cep": None,
                    "complemento": None,
                    "cidade": None,
                }

                tipos = [
                    "diaria",
                    "adiantamento",
                    "adiantamento_insumo",
                    "adiantamento_combustivel",
                    "veiculo",
                    "passagem",
                    "rpa",
                    "produto",
                    "servico",
                    "outro",
                    "nao_se_aplica",
                ]

                if record_escola != "Departamento" and record_escola != "CETT COTEC" and record_escola:
                    escola_nome = process.extractOne(record_escola, [nome for id, nome in escolas], scorer=fuzz.ratio)
                    escola_id = escola_dict.get(escola_nome[0])
                    importData["escola"] = escola_id
                else:
                    importData["escola"] = None
               
                
                if record_beneficiario:
                    pessoa_nome = process.extractOne(record_beneficiario, [nome for id, nome in pessoas], scorer=fuzz.ratio)
                    pessoa_id = pessoa_dict.get(pessoa_nome[0])
                    importData["beneficiario"] = pessoa_id
                else:
                    importData["beneficiario"] = None
                
                if record_tipo:
                    tipo_nome = process.extractOne(record_tipo, tipos, scorer=fuzz.ratio)
                    importData["tipo"] = tipo_nome[0]
                else:
                    importData["tipo"] = None
                
                if record_data_inicio:
                    importData["data_inicio"] = record_data_inicio
                else:
                    importData["data_inicio"] = None

                data_to_import.append(importData)
                table_data.append(row_data)
            return render(request, 'demandas/importar_demanda_modal.html', {"data": data_to_import, "row_data": table_data})
    return render(request, 'demandas/importar_demanda_modal.html')