from contextlib import redirect_stderr
from pyexpat.errors import messages
from django.shortcuts import render, redirect
from sistema.serializers.alocacaoSerializer import AlocacaoSerializer
from sistema.serializers.cursoSerializer import CursoSerializer
from sistema.serializers.pessoaSerializer import PessoaSerializer
from sistema.serializers.eventoSerializer import EventoSerializer
from sistema.models.pessoa import Pessoas
from sistema.models.alocacao import Alocacao
from django.db.models import Prefetch, Count
from sistema.models.curso import Curso
from sistema.models.evento import Evento
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
    evento_id = request.GET.get('evento_id')
    alocacoes = Alocacao.objects
    if evento_id:
        alocacoes = alocacoes.filter(evento_id = evento_id)
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
        eventos = Evento.objects.filter(~Q(status="finalizado"))
        eventos = EventoSerializer(eventos, many=True)
        data['eventos'] = eventos.data
    return render(request,'pessoas/modal_alocar_pessoa.html',data)

@login_required(login_url='/auth-user/login-user')
def alocacaoModalCadastrar(request):
    id = request.GET.get('id')
    alocacao = None
    data = {}
    if id:
        alocacao = Alocacao.objects.get(id=id)
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
 
def intervening_weekdays(start, end, inclusive=True, weekdays=[0, 1, 2, 3, 4, 5, 6]):
    if isinstance(start, datetime.datetime):
        start = start.date()               # make a date from a datetime

    if isinstance(end, datetime.datetime):
        end = end.date()                   # make a date from a datetime

    if end < start:
        # you can opt to return 0 or swap the dates around instead
        raise ValueError("start date must be before end date")

    if inclusive:
        end += datetime.timedelta(days=1)  # correct for inclusivity

    try:
        # collapse duplicate weekdays
        weekdays = {weekday % 7 for weekday in weekdays}
    except TypeError:
        weekdays = [weekdays % 7]

    ref = datetime.date.today()                    # choose a reference date
    ref -= datetime.timedelta(days=ref.weekday())  # and normalize its weekday

    # sum up all selected weekdays (max 7 iterations)
    return sum((ref_plus - start).days // 7 - (ref_plus - end).days // 7
            for ref_plus in
            (ref + datetime.timedelta(days=weekday) for weekday in weekdays))
        

@login_required(login_url='/auth-user/login-user')
def horasTrabalhadas(request):
    print("dentro de horas trabalhadas", request.GET.get('data_inicio'), request.GET.get('data_fim'))
    data_inicio = request.GET.get('data_inicio')
    data_fim = request.GET.get('data_fim')
    pessoas = Pessoas.objects
    if data_fim and data_inicio:
        pessoas = pessoas.prefetch_related(
            Prefetch("alocacao_set", queryset=
                Alocacao.objects.filter(
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
        for alocacao in pessoa['alocacao_set']:
            cargaHorariaDia = 0
            for turno in alocacao['turnos']:
                cargaHorariaDia += turno["carga_horaria"]
            
            alocacaoDataInicio = datetime.datetime.strptime(alocacao['data_inicio'], '%Y-%m-%d')
            alocacaoDataFim = datetime.datetime.strptime(alocacao['data_fim'], '%Y-%m-%d')
            queryDataInicio = datetime.datetime.strptime(data_inicio, '%Y-%m-%d')
            queryDataFim = datetime.datetime.strptime(data_fim, '%Y-%m-%d')

            inicio = alocacaoDataInicio if alocacaoDataInicio >= queryDataInicio else queryDataInicio
            fim = alocacaoDataFim if alocacaoDataFim <= queryDataFim else queryDataFim 

            week_day =  {
                'segunda': intervening_weekdays(inicio, fim, True, [0]),
                'terca': intervening_weekdays(inicio, fim, True, [1]),
                'quarta': intervening_weekdays(inicio, fim, True, [2]),
                'quinta': intervening_weekdays(inicio, fim, True, [3]),
                'sexta': intervening_weekdays(inicio, fim, True, [4]),
                'sabado': intervening_weekdays(inicio, fim, True, [5]),
                'domingo': intervening_weekdays(inicio, fim, True, [6])
            }
           
            sabado = week_day["sabado"] if alocacao["aulas_sabado"] else 0
            diasTranscorridos = week_day["segunda"] + week_day["terca"] + week_day["quarta"] + week_day["quinta"] + week_day["sexta"] + sabado
            alocacao['horas_trabalhadas'] = diasTranscorridos * cargaHorariaDia
            total_horas_pessoa += alocacao['horas_trabalhadas']
        pessoa['total_horas'] = total_horas_pessoa
        if pessoa['cargo'] == 'professor':
            tabela_horas_trabalhadas.append({"nome": nome, "cpf": cpf, "total_horas": total_horas_pessoa})
    print(tabela_horas_trabalhadas)

    response = HttpResponse(
        content_type='text/csv',
        headers={'Content-Disposition': 'attachment; filename="somefilename.csv"'},
    )

    output = io.BytesIO()
    workbook = xlsxwriter.Workbook(output)
    worksheet = workbook.add_worksheet()
    worksheet.write(0, 0, 'Nome')
    worksheet.write(0, 1, 'CPF')
    worksheet.write(0, 2, 'Total de Horas')
    for row_num, columns in enumerate(tabela_horas_trabalhadas):
        for col_num, cell_data in enumerate(columns):
            worksheet.write(row_num+1, col_num, columns[cell_data])
    
    workbook.close()
    output.seek(0)

    filename = 'django_simple.xlsx'
    response = HttpResponse(
        output,
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )

    response['Content-Disposition'] = 'attachment; filename=%s' % filename
    return response