from contextlib import redirect_stderr
from pyexpat.errors import messages
from django.shortcuts import render, redirect
from sistema.serializers.cursoSerializer import CursoSerializer
from sistema.models.pessoa import Pessoas
from sistema.models.curso import Curso
from django.contrib import messages
from django.contrib.auth.decorators import login_required
import requests
import json
from django.http import JsonResponse
from rest_framework.authtoken.models import Token

# Create your views here. teste

@login_required(login_url='/auth-user/login-user')
def gerencia_cursos(request):
    page_title = "Cursos"
    count = 0
    cursos = Curso.objects.all()
    for p in cursos:
        count += 1

    return render(request,'cursos/gerencia_cursos.html',
    {'cursos':cursos,'contagem':count, "page_title": page_title})

@login_required(login_url='/auth-user/login-user')
def cursosTable(request):
    nome = request.GET.get('nome')
    cursos = Curso.objects
    if nome:
        cursos = cursos.filter(nome__contains = nome)
    cursos = cursos.all()
    return render(request,'cursos/cursos_table.html',{'cursos':cursos})

@login_required(login_url='/auth-user/login-user')
def visualizarCurso(request,codigo):
    curso = Curso.objects.get(id=codigo)
    return render(request,'cursos/visualizar_curso.html',{'curso':curso})

@login_required(login_url='/auth-user/login-user')
def cursosModalCadastrar(request):
    id = request.GET.get('id')
    curso = None
    data = {}
    if id:
        curso = Curso.objects.get(id=id)
        data['curso'] = curso
    return render(request,'cursos/modal_cadastrar_curso.html',data)

@login_required(login_url='/auth-user/login-user')
def cursosSelect(request):
    cursos = Curso.objects.all()
    return render(request,'pessoas/cursos_select.html',{'cursos':cursos})

@login_required(login_url='/auth-user/login-user')
def eliminarCurso(request,codigo):
    curso = Curso.objects.get(id=codigo)
    curso.delete()
    return redirect('/gerenciar-cursos')

@login_required(login_url='/auth-user/login-user')
def saveCurso(request):
    token, created = Token.objects.get_or_create(user=request.user)
    headers = {'Authorization': 'Token ' + token.key}
    body = json.loads(request.body)['data']
    response = requests.post('http://localhost:8000/cursos', json=body, headers=headers)
    return JsonResponse(json.loads(response.content),status=response.status_code)

@login_required(login_url='/auth-user/login-user')
def editarCurso(request, codigo):
    token, created = Token.objects.get_or_create(user=request.user)
    headers = {'Authorization': 'Token ' + token.key}
    body = json.loads(request.body)['data']
    response = requests.put('http://localhost:8000/cursos/'+str(codigo), json=body, headers=headers)
    return JsonResponse(json.loads(response.content),status=response.status_code)
