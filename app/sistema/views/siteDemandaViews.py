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