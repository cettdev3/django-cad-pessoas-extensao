from django.shortcuts import render
from sistema.models import Pessoas, Curso
from django.contrib.auth.decorators import login_required
from django.forms.models import model_to_dict
import json
from django.http import JsonResponse

@login_required(login_url="/auth-user/login-user")
def projetoCotecIndex(request):
    page_title = "Projetos de Extensão"
    return render(                  
        request,
        "projetosCotec/projetosCotecIndex.html",
        {"page_title": page_title},
    )


@login_required(login_url="/auth-user/login-user")
def projetoCotecForm(request):
    page_title = "Novo Projeto de Extensão"
    pessoas = Pessoas.objects.all()
    pessoas_list = list(pessoas.values('id', 'nome')) 
    pessoas_json = json.dumps(pessoas_list)

    cursos = Curso.objects.all()
    cursos_list = list(cursos.values('id', 'nome'))
    cursos_json = json.dumps(cursos_list)

    return render(
        request,
        "projetosCotec/projetoCotecCreate.html",
        {
            "page_title": page_title,
            "pessoas": pessoas_json,
            "cursos": cursos_json,
        },
    )

@login_required(login_url="/auth-user/login-user")
def pessoaModal(request):
    id = "cotec"
    instituicoes = Pessoas.INSTITUICAO_CHOICES
    return render(
        request,
        "pessoas/form_pessoa.html",
        {
            "id": id,
            "instituicoes": instituicoes,
        },
    )

@login_required(login_url="/auth-user/login-user")
def pessoaCreate(request):
    data = json.loads(request.body.decode())
    pessoa = Pessoas()
    pessoa.nome = data.get("nome")
    pessoa.email = data.get("email")
    pessoa.telefone = data.get("telefone")
    pessoa.cpf = data.get("cpf")
    pessoa.save()  # Save the pessoa object to the database
    pessoa_dict = model_to_dict(pessoa)  # Convert the pessoa object to a dictionary
    return JsonResponse(pessoa_dict) 
