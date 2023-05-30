from pyexpat.errors import messages
from django.shortcuts import render, redirect
from sistema.models.pessoa import Pessoas
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from rest_framework.authtoken.models import Token
import json
import datetime
import requests
    
@login_required(login_url='/auth-user/login-user')
def calendario(request):
    return render(request, 'componentes/calendario/calendario.html')

@login_required(login_url='/auth-user/login-user')
def filtrosRelatorioEventosModal(request):
    return render(request, 'componentes/filtrosRelatorioEventosModal/filtrosRelatorioEventosModal.html')

@login_required(login_url='/auth-user/login-user')
def confirmDeleteModal(request):
    return render(request, 'componentes/confirmDeleteModal/confirmDeleteModal.html')

@login_required(login_url='/auth-user/login-user')
def filterMultipleSelect(request):
    route = request.GET.get('route')
    label = request.GET.get('label')
    placeholder = request.GET.get('placeholder')
    id = request.GET.get('id')
    if not route:
        route = "cursos"
    if not label:
        label = "Label teste"
    if not placeholder:
        placeholder = "Placeholder teste"
    if not id:
        id = "select-multiple-dropdown"

    token, created = Token.objects.get_or_create(user=request.user)
    headers = {'Authorization': 'Token ' + token.key}
    response = requests.get('http://localhost:8000/'+route, headers=headers)
    items = json.loads(response.content)
    return render(request,'componentes/selectMultipleFilter/selectMultipleFilter.html',{
        'items':items, 
        'label':label, 
        'placeholder':placeholder,
        'id':id
    })