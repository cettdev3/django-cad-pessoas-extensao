from contextlib import redirect_stderr
from pyexpat.errors import messages
from django.shortcuts import render, redirect
from sistema.serializers.alocacaoSerializer import AlocacaoSerializer
from sistema.serializers.cursoSerializer import CursoSerializer
from sistema.serializers.pessoaSerializer import PessoaSerializer
from sistema.serializers.ensinoSerializer import EnsinoSerializer
from sistema.models.pessoa import Pessoas
from sistema.models.alocacao import Alocacao
from django.db.models import Prefetch, Count
from sistema.models.curso import Curso
from sistema.models.ensino import Ensino
from django.contrib import messages
from django.contrib.auth.decorators import login_required
import requests
from django.db.models import Q, Exists
import json
import datetime
import xlsxwriter
import io
from django.http import JsonResponse
from rest_framework.authtoken.models import Token
from django.http import HttpResponse

@login_required(login_url='/auth-user/login-user')
def alocacoesTable(request):
    acaoEnsino_id = request.GET.get('acaoEnsino_id')
    alocacoes = Alocacao.objects
    if acaoEnsino_id:
        alocacoes = alocacoes.filter(acaoEnsino_id = acaoEnsino_id)
    alocacoes = alocacoes.all()
    return render(request,'alocacoes/alocacoes_table.html',{'alocacoes':alocacoes})

@login_required(login_url='/auth-user/login-user')
def modalAlocar(request):
    pessoaIds = request.GET.getlist('checked_values[]')
    data = {}
    if pessoaIds:
        pessoas = Pessoas.objects.filter(id__in=pessoaIds).all()
        pessoas = PessoaSerializer(pessoas, many = True)
        data['pessoas'] = pessoas.data
        ensinos = Ensino.objects.filter(~Q(status="finalizado"))
        ensinos = EnsinoSerializer(ensinos, many=True)
        data['ensinos'] = ensinos.data
    return render(request,'pessoas/modal_alocar_pessoa.html',data)

@login_required(login_url='/auth-user/login-user')
def alocacaoModalCadastrar(request):
    id = request.GET.get('id')
    alocacao = None
    data = {}
    if id:
        alocacao = Alocacao.objects.prefetch_related("dataremovida_set").get(id=id)
        alocacao = AlocacaoSerializer(alocacao).data
        data['alocacao'] = alocacao
    return render(request,'alocacoes/modal_cadastrar_alocacao.html',data)

@login_required(login_url='/auth-user/login-user')
def saveAlocacao(request):
    token, created = Token.objects.get_or_create(user=request.user)
    headers = {'Authorization': 'Token ' + token.key}
    body = json.loads(request.body)['data']
    response = requests.post('http://localhost:8000/alocacoes', json=body, headers=headers)
    return JsonResponse(json.loads(response.content.decode()),status=response.status_code, safe=False)

@login_required(login_url='/auth-user/login-user')
def editarAlocacao(request, codigo):
    token, created = Token.objects.get_or_create(user=request.user)
    headers = {'Authorization': 'Token ' + token.key}
    body = json.loads(request.body)['data']
    response = requests.put('http://localhost:8000/alocacoes/'+str(codigo), json=body, headers=headers)
    return JsonResponse(json.loads(response.content),status=response.status_code)

@login_required(login_url='/auth-user/login-user')
def eliminarAlocacao(request,codigo):
    token, created = Token.objects.get_or_create(user=request.user)
    headers = {'Authorization': 'Token ' + token.key}
    response = requests.delete('http://localhost:8000/alocacoes/'+str(codigo), headers=headers)
    
    return HttpResponse(status=response.status_code)

@login_required(login_url='/auth-user/login-user')
def horasTrabalhadas(request):
    body = json.loads(request.body.decode())
    data_inicio = body['data_inicio']
    data_fim = body['data_fim']
    removed_dates = body['removed_dates']
    pessoas = Pessoas.objects
    if data_fim and data_inicio:
        pessoas = pessoas.prefetch_related(
            Prefetch("alocacao_set", queryset=
                Alocacao.objects.prefetch_related("dataremovida_set").filter(
                   Q(
                        Q(data_inicio__gte=data_inicio,data_inicio__lte=data_fim) |
                        Q(data_fim__gte=data_inicio,data_fim__lte=data_fim) |
                        Q(data_inicio__lte=data_inicio,data_fim__gte=data_inicio) |
                        Q(data_inicio__lte=data_fim,data_fim__gte=data_fim)
                    )
                )
            )
        )
    pessoas = pessoas.filter(alocacao__isnull=False).distinct().all()
    serializer = PessoaSerializer(pessoas, many=True)

    tabela_horas_trabalhadas = []
    for pessoa in serializer.data:
        nome = pessoa['nome']
        cpf = pessoa['cpf']
        total_horas_pessoa = 0
        carga_horaria_dia = {}
        queryDataInicio = datetime.datetime.strptime(data_inicio, '%Y-%m-%d')
        queryDataFim = datetime.datetime.strptime(data_fim, '%Y-%m-%d')
        
        while queryDataInicio <= queryDataFim:
            carga_horaria_dia[queryDataInicio.strftime('%Y-%m-%d')] = {
                'carga_horaria': 0
            }
            queryDataInicio += datetime.timedelta(days=1)
        
        for alocacao in pessoa['alocacao_set']:
            alocacao['horas_trabalhadas'] = 0
            datasRemovidas = [item["date"] for item in alocacao["dataremovida_set"]]
            cargaHorariaDia = 0
            for turno in alocacao['turnos']:
                cargaHorariaDia += turno["carga_horaria"]
            
            queryDataInicio = datetime.datetime.strptime(data_inicio, '%Y-%m-%d')
            queryDataFim = datetime.datetime.strptime(data_fim, '%Y-%m-%d')
            alocacaoDataInicio = datetime.datetime.strptime(alocacao['data_inicio'], '%Y-%m-%d')
            alocacaoDataFim = datetime.datetime.strptime(alocacao['data_fim'], '%Y-%m-%d')

            while queryDataInicio <= queryDataFim:
                isSatturday = queryDataInicio.weekday() == 5
                count_sabado = (not isSatturday) or alocacao["aulas_sabado"]
                is_alocation_date = queryDataInicio >= alocacaoDataInicio and queryDataInicio <= alocacaoDataFim 
                is_sunday = queryDataInicio.weekday() == 6
                if queryDataInicio.strftime('%Y-%m-%d') not in removed_dates and queryDataInicio.strftime('%Y-%m-%d') not in datasRemovidas and count_sabado and is_alocation_date and not is_sunday:
                    chave = queryDataInicio.strftime('%Y-%m-%d')
                    carga_horaria_dia[chave]["carga_horaria"] += cargaHorariaDia
                    total_horas_pessoa += cargaHorariaDia
                    alocacao['horas_trabalhadas'] += cargaHorariaDia
                
                queryDataInicio += datetime.timedelta(days=1)

        pessoa['total_horas'] = total_horas_pessoa
        if pessoa['cargo'] == 'professor':
            tabela_horas_trabalhadas.append({"nome": nome, "cpf": cpf, "carga_horaria_dia": carga_horaria_dia,"total_horas": total_horas_pessoa})
    
    response = HttpResponse(
        content_type='text/csv',
        headers={'Content-Disposition': 'attachment; filename="somefilename.csv"'},
    )

    output = io.BytesIO()
    workbook = xlsxwriter.Workbook(output)
    worksheet = workbook.add_worksheet()
    worksheet.write(0, 0, 'Nome')
    worksheet.write(0, 1, 'CPF')
    worksheet.write(0, len(tabela_horas_trabalhadas[0]['carga_horaria_dia'])+2, 'Total de Horas')
    for i, date in enumerate(tabela_horas_trabalhadas[0]['carga_horaria_dia']):
        date = date.split('-')
        date = date[2] + '/' + date[1] + '/' + date[0]
        worksheet.write(0, i+2, date)

    for pessoa in tabela_horas_trabalhadas:
        worksheet.write(tabela_horas_trabalhadas.index(pessoa)+1, 0, pessoa['nome'])
        worksheet.write(tabela_horas_trabalhadas.index(pessoa)+1, 1, pessoa['cpf'])
        for i, date in enumerate(pessoa['carga_horaria_dia']):
            worksheet.write(tabela_horas_trabalhadas.index(pessoa)+1, i+2, pessoa['carga_horaria_dia'][date]['carga_horaria'])
        worksheet.write(tabela_horas_trabalhadas.index(pessoa)+1, len(pessoa['carga_horaria_dia'])+2, pessoa['total_horas'])


    workbook.close()
    output.seek(0)

    filename = 'django_simple.xlsx'
    response = HttpResponse(
        output,
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )

    response['Content-Disposition'] = 'attachment; filename=%s' % filename
    return response