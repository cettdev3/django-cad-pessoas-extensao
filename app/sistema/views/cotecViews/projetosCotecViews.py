from django.shortcuts import render, redirect
from sistema.models import Pessoas, Curso, Atividade, Cidade, MembroExecucao, OrcamentoItem, Orcamento
from django.contrib.auth.decorators import login_required
from django.forms.models import model_to_dict
import json
from django.http import JsonResponse
from sistema.models import PropostaProjeto, DpEvento, DpEventoEscola, Escola, Galeria, AtividadeSection, AtividadeCategoria
from django.db import transaction
import requests
from rest_framework.authtoken.models import Token
from django.core.exceptions import ObjectDoesNotExist
from sistema.emailtemplates import PropostaSubmetidaEmail
from django.core import serializers
from django.db.models import Q

@login_required(login_url="/auth-user/login-user")
def projetoCotecIndex(request):
    user = request.user
    pessoa = Pessoas.objects.get(user=user)
    page_title = "Propostas de Projetos"
    return render(                  
        request,
        "projetosCotec/projetosCotecIndex.html",
        {
            "page_title": page_title,
            "pessoa": pessoa,
        },
    )

@login_required(login_url="/auth-user/login-user")
def projetoCotecSuccess(request):
    propostaId = request.GET.get("proposta_id")
    context = {}
    if propostaId:
        context['proposta'] = PropostaProjeto.objects.get(pk=propostaId)
    return render(
        request,
        "projetosCotec/propostaCreateSuccess.html",
        context,
    )

@login_required(login_url="/auth-user/login-user")
def projetoCotecForm(request):
    proposta_id = request.GET.get("proposta_id")
    page_title = "Nova Proposta de Projeto de Extensão" if not proposta_id else "Editar Proposta de Projeto de Extensão"
    pessoas = Pessoas.objects.all()
    pessoas_list = list(pessoas.values('id', 'nome')) 
    pessoas_json = json.dumps(pessoas_list)
    proposta_projeto = None
    user = request.user
    pessoa = Pessoas.objects.get(user=user)
    if proposta_id:
        proposta_projeto = PropostaProjeto.objects.get(pk=proposta_id)
    else:
        proposta_projeto =  handlePropostaProjetoCreate({"status": PropostaProjeto.STATUS_RASCUNHO}, pessoa)

    cidades = Cidade.objects.all()
    cidades_list = list(cidades.values('id', 'nome'))
    cidades_json = json.dumps(cidades_list)
    cursos = Curso.objects.all()
    cursos_list = list(cursos.values('id', 'nome'))
    cursos_json = json.dumps(cursos_list)
    proponentes_json = serializers.serialize('json', proposta_projeto.proponentes)
    responsaveis_json = serializers.serialize('json', proposta_projeto.responsaveis)
    atividades_json = serializers.serialize('json', proposta_projeto.atividades.all())
    equipe_json = serializers.serialize('json', proposta_projeto.equipe.filter(~Q(role__in=["proponente", "responsavel"])))
    orcamento_itens_json = serializers.serialize('json', proposta_projeto.orcamento.items.all())
    return render(
        request,
        "projetosCotec/projetoCotecCreate.html",
        {
            "page_title": page_title,
            "pessoas": pessoas_json,
            "cursos": cursos_json,
            "cidades": cidades_json,
            "proposta_projeto": proposta_projeto,
            "proponentes_json": proponentes_json,
            "responsaveis_json": responsaveis_json,
            "atividades_json": atividades_json,
            "equipe_json": equipe_json,
            "orcamento_itens_json": orcamento_itens_json,
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
    pessoa.save()
    pessoa_dict = model_to_dict(pessoa)
    return JsonResponse(pessoa_dict) 


@login_required(login_url="/auth-user/login-user")
def selectMultipleComponent(request):
    context = {}
    context["model"] = request.GET.get("model")
    context["id"] = request.GET.get("id")
    context["modal_label"] = request.GET.get("modal_label")
    context["select_label"] = request.GET.get("select_label")
    context["multiple"] = request.GET.get("multiple")

    return render(
        request,
        "projetosCotec/customSelectMultiple.html",
        context,
    )

@login_required(login_url="/auth-user/login-user")
def getMultipleFormComponent(request):
    context = {}
    return render(
        request,
        "projetosCotec/multipleFormComponent.html",
        context,
    )

@login_required(login_url="/auth-user/login-user")
def membroEquipeForm(request):
    model_id = request.GET.get("model_id")
    escola_nome = request.GET.get("escola_nome")
    context = {}
    context["escola_nome"] = escola_nome
    if model_id:
        try:
            membroEquipe = MembroExecucao.objects.get(pk=model_id)
            context["membroEquipe"] = membroEquipe
        except ObjectDoesNotExist:
            return JsonResponse({"message": "Membro da equipe não encontrado"}, status=400)
    return render(
        request,
        "projetosCotec/membroEquipeForm.html",
        context,
    )

def handlePropostaProjetoCreate(data, pessoa):
    with transaction.atomic():
        orcamento = Orcamento()
        orcamento.save()
        proposta_projeto = PropostaProjeto()
        proposta_projeto.titulo_projeto = data.get("titulo_projeto")
        if data.get("data_inicio"):
            proposta_projeto.data_inicio = data.get("data_inicio")
        if data.get("data_fim"):
            proposta_projeto.data_fim = data.get("data_fim")
        proposta_projeto.resumo_proposta = data.get("resumo_proposta")
        proposta_projeto.objetivos_gerais = data.get("objetivos_gerais")
        proposta_projeto.objetivos_especificos = data.get("objetivos_especificos")
        proposta_projeto.metodologia = data.get("metodologia")
        proposta_projeto.formato_conteudo = data.get("formato_conteudo")
        proposta_projeto.justificativas = data.get("justificativas")
        proposta_projeto.resultados_esperados = data.get("resultados_esperados")
        proposta_projeto.fontes_apoio = data.get("fontes_apoio")
        proposta_projeto.informacoes_adicionais = data.get("informacoes_adicionais")
        proposta_projeto.publico_alvo = data.get("publico_alvo")
        proposta_projeto.orcamento = orcamento
        proposta_projeto.escola = pessoa.escola
        if data.get("status"):
            proposta_projeto.status = data.get("status")
        else:
            proposta_projeto.status = PropostaProjeto.STATUS_EM_ANALISE_DIRECAO
        proposta_projeto.save() 
        if data.get("cronograma"):
            for atividade in data.get("cronograma"):
                db_atividade = Atividade()
                if atividade.get("cidade_id"):
                    db_atividade.cidade = Cidade.objects.get(pk=atividade.get("cidade_id"))
                db_atividade.data_realizacao_inicio = atividade.get("data")
                db_atividade.horario_inicio = atividade.get("hora")
                db_atividade.local = atividade.get("local")
                db_atividade.nome = atividade.get("nome")
                db_atividade.publico_esperado = atividade.get("publico_esperado")
                db_atividade.proposta_projeto = proposta_projeto
                db_atividade.save()

        if data.get("equipe"):
            for membro_equipe in data.get("equipe"):
                db_membro_equipe = MembroExecucao()
                if membro_equipe.get("data_inicio"):
                    db_membro_equipe.data_inicio = membro_equipe.get("data_inicio")
                db_membro_equipe.proposta_projeto = proposta_projeto
                db_membro_equipe.role = membro_equipe.get("role")
                db_membro_equipe.instituicao = membro_equipe.get("instituicao")
                if membro_equipe.get("pessoa_id"):
                    db_membro_equipe.pessoa = Pessoas.objects.get(pk=membro_equipe.get("pessoa_id"))
                db_membro_equipe.save()
            
        if data.get("proponente"):
            for membro_equipe in data.get("proponente"):
                db_membro_equipe = MembroExecucao()
                if membro_equipe.get("pessoa_id"):
                    db_membro_equipe.pessoa = Pessoas.objects.get(pk=membro_equipe.get("pessoa_id"))
                db_membro_equipe.proposta_projeto = proposta_projeto
                db_membro_equipe.role = "proponente"
                db_membro_equipe.instituicao = membro_equipe.get("instituicao")
                db_membro_equipe.save()
        else:
            db_membro_equipe = MembroExecucao()
            db_membro_equipe.proposta_projeto = proposta_projeto
            db_membro_equipe.role = "proponente"
            db_membro_equipe.save()

        if data.get("responsavel"):
            for membro_equipe in data.get("responsavel"):
                db_membro_equipe = MembroExecucao()
                if membro_equipe.get("pessoa_id"):
                    db_membro_equipe.pessoa = Pessoas.objects.get(pk=membro_equipe.get("pessoa_id"))
                db_membro_equipe.proposta_projeto = proposta_projeto
                db_membro_equipe.role = "responsavel"
                db_membro_equipe.instituicao = membro_equipe.get("instituicao")
                db_membro_equipe.save()

        if data.get("orcamento"):
            for orcamento_item in data.get("orcamento"):
                db_orcamento_item = OrcamentoItem()
                db_orcamento_item.orcamento = orcamento
                db_orcamento_item.descricao = orcamento_item.get('descricao')
                db_orcamento_item.tipo = orcamento_item.get('tipo')
                db_orcamento_item.quantidade = orcamento_item.get('quantidade')
                db_orcamento_item.unidade = orcamento_item.get('unidade')
                db_orcamento_item.valor = orcamento_item.get('valor')
                db_orcamento_item.valor_total = orcamento_item.get('valor_total')
                db_orcamento_item.save()    
        return proposta_projeto

@login_required(login_url="/auth-user/login-user")
def createPropostaProjeto(request): 
    data = json.loads(request.body.decode())
    user = request.user
    pessoa = Pessoas.objects.get(user=user)
    print(pessoa.nome)
    if not pessoa.escola:
        return JsonResponse({"message": "Você precisa estar vinculado a uma escola para submeter uma proposta"}, status=400)
    
    proposta_projeto = handlePropostaProjetoCreate(data, pessoa)
    if proposta_projeto.status == PropostaProjeto.STATUS_EM_ANALISE_DIRECAO:
        try:
            success = PropostaSubmetidaEmail(proposta_projeto).send()
        except Exception as e:
            print(e)
        

    return redirect('cotec-projeto-index')

@login_required(login_url="/auth-user/login-user")
def updatePropostaProjeto(request, pk): 
    data = json.loads(request.body.decode())
    proposta_projeto = PropostaProjeto.objects.get(pk=pk)
    if data.get("titulo_projeto"):
        proposta_projeto.titulo_projeto = data.get("titulo_projeto")
    if data.get("data_inicio"):
        proposta_projeto.data_inicio = data.get("data_inicio")
    if data.get("data_fim"):
        proposta_projeto.data_fim = data.get("data_fim")
    if data.get("resumo_proposta"):
        proposta_projeto.resumo_proposta = data.get("resumo_proposta")
    if data.get("objetivos_gerais"):
        proposta_projeto.objetivos_gerais = data.get("objetivos_gerais")
    if data.get("objetivos_especificos"):
        proposta_projeto.objetivos_especificos = data.get("objetivos_especificos")
    if data.get("metodologia"):
        proposta_projeto.metodologia = data.get("metodologia")
    if data.get("formato_conteudo"):
        proposta_projeto.formato_conteudo = data.get("formato_conteudo")
    if data.get("justificativas"):
        proposta_projeto.justificativas = data.get("justificativas")
    if data.get("resultados_esperados"):
        proposta_projeto.resultados_esperados = data.get("resultados_esperados")
    if data.get("fontes_apoio"):
        proposta_projeto.fontes_apoio = data.get("fontes_apoio")
    if data.get("informacoes_adicionais"):
        proposta_projeto.informacoes_adicionais = data.get("informacoes_adicionais")
    if data.get("publico_alvo"):
        proposta_projeto.publico_alvo = data.get("publico_alvo")
    if data.get("status"):
        print("dentro de set status: ", data.get("status"))
        proposta_projeto.status = data.get("status")
    if data.get("justificativa"):
        proposta_projeto.justificativas = data.get("justificativa")
    proposta_projeto.save() 
    proposta_projeto = model_to_dict(proposta_projeto)
    return JsonResponse(proposta_projeto)

@login_required(login_url="/auth-user/login-user")
def showPropostaProjeto(request, pk): 
    pessoa = Pessoas.objects.get(user=request.user)
    proposta_projeto = PropostaProjeto.objects.get(pk=pk)
    page_title = "Proposta de Projeto de Extensão"
    return render(
        request,
        "projetosCotec/projetosCotecPropostaShow.html",
        {
            "proposta_projeto": proposta_projeto,
            "pessoa": pessoa,
            "page_title": page_title,
        },
    )

@login_required(login_url="/auth-user/login-user")
def removePropostaProjeto(request, pk):
    proposta_projeto = PropostaProjeto.objects.get(pk=pk)
    with transaction.atomic():
        orcamento = proposta_projeto.orcamento
        if orcamento:
            orcamento_items = OrcamentoItem.objects.filter(orcamento=orcamento)
            for item in orcamento_items:
                item.delete()
            orcamento.delete()
        atividades = proposta_projeto.atividades.all()
        for atividade in atividades:
            atividade.delete()
        membros_equipe = proposta_projeto.equipe.all()
        for membro_equipe in membros_equipe:
            membro_equipe.delete()

        proposta_projeto.delete()
    return JsonResponse({"message": "Proposta removida com sucesso!"})

@login_required(login_url="/auth-user/login-user")
def propostasTable(request):
    user = request.user
    pessoa = Pessoas.objects.get(user=user)
    
    propostas = PropostaProjeto.objects.prefetch_related(
        'orcamento', 
        'equipe', 
        'atividades'
        )
    if pessoa.instituicao != "cett" and pessoa.escola:
        propostas = propostas.filter(escola=pessoa.escola)
    if pessoa.instituicao == "cett":
        propostas = propostas.exclude(status=PropostaProjeto.STATUS_RASCUNHO)
    propostas = propostas.all()
    return render(
        request,
        "projetosCotec/projetosCotecPropostaTable.html",
        {
            "propostas": propostas,
            "pessoa": pessoa,
        },
    )

@login_required(login_url="/auth-user/login-user")
def updateAtividade(request, pk):
    data = json.loads(request.body.decode())
    atividade = Atividade.objects.get(pk=pk)
    if data.get("data_realizacao_inicio"):
        atividade.data_realizacao_inicio = data.get("data_realizacao_inicio")
    if data.get("horario_inicio"):
        atividade.horario_inicio = data.get("horario_inicio")
    if data.get("horario_fim"):
        atividade.horario_fim = data.get("horario_fim")
    if data.get("local"):
        atividade.local = data.get("local")
    if data.get("nome"):
        atividade.nome = data.get("nome")
    if data.get("publico_esperado"):
        atividade.publico_esperado = data.get("publico_esperado")
    if data.get("cidade_id"):
        atividade.cidade = Cidade.objects.get(pk=data.get("cidade_id"))
    atividade.save()
    atividade = model_to_dict(atividade)
    return JsonResponse(atividade)

@login_required(login_url="/auth-user/login-user")
def createAtividade(request):
    data = json.loads(request.body.decode())
    atividade = Atividade()
    if data.get("data"):
        atividade.data_realizacao_inicio = data.get("data")
    if data.get("hora"):
        atividade.horario_inicio = data.get("hora")
    if data.get("local"):
        atividade.local = data.get("local")
    if data.get("nome"):
        atividade.nome = data.get("nome")
    if data.get("publico_esperado"):
        atividade.publico_esperado = data.get("publico_esperado")
    atividade.proposta_projeto = PropostaProjeto.objects.get(pk=data.get("proposta_projeto_id"))
    if data.get("cidade_id"):
        atividade.cidade = Cidade.objects.get(pk=data.get("cidade_id"))
    atividade.save()
    atividade = model_to_dict(atividade)
    return JsonResponse(atividade)

@login_required(login_url="/auth-user/login-user")
def removeAtividade(request, pk):
    atividade = Atividade.objects.get(pk=pk)
    atividade.delete()
    return JsonResponse({"message": "Atividade removida com sucesso!"})

@login_required(login_url="/auth-user/login-user")
def updateMembroEquipe(request, pk):
    payload = json.loads(request.body)
    token, created = Token.objects.get_or_create(user=request.user)
    headers = {'Authorization': 'Token ' + token.key}
    url = 'http://localhost:8000/membroExecucao/'+str(pk)
    body = payload
    response = requests.put(url, json=body, headers=headers)

    membro_equipe = json.loads(response.content)
    return JsonResponse(membro_equipe)

@login_required(login_url="/auth-user/login-user")
def createMembroEquipe(request):
    payload = json.loads(request.body) if request.body else {}
    token, created = Token.objects.get_or_create(user=request.user)
    headers = {'Authorization': 'Token ' + token.key}
    url = 'http://localhost:8000/membroExecucao'
    body = payload
    response = requests.post(url, json=body, headers=headers)
    membro_equipe_response = json.loads(response.content)
    
    if response.status_code != 200 and response.status_code != 201:
        return JsonResponse(membro_equipe_response, status=400, safe=False)
    return JsonResponse(membro_equipe_response)

@login_required(login_url="/auth-user/login-user")
def removeMembroEquipe(request, pk):
    atividade = MembroExecucao.objects.get(pk=pk)
    atividade.delete()
    return JsonResponse({"message": "Atividade removida com sucesso!"})

@login_required(login_url="/auth-user/login-user")
def updateItemOrcamento(request, pk):
    print("data dentro de update item orcamento: ", request.body.decode())
    data = json.loads(request.body.decode())
    itemOrcamento = OrcamentoItem.objects.get(pk=pk)
    if data.get('descricao'):
        itemOrcamento.descricao = data.get('descricao')
    if data.get('tipo'):
        itemOrcamento.tipo = data.get('tipo')
    if data.get('quantidade'):
        itemOrcamento.quantidade = data.get('quantidade')
    if data.get('unidade'):
        itemOrcamento.unidade = data.get('unidade')
    if data.get('valor'):
        itemOrcamento.valor = data.get('valor')
    if 'em_estoque' in data:
        itemOrcamento.em_estoque = data.get('em_estoque')
    if data.get('valor_total'):
        itemOrcamento.valor_total = data.get('valor_total')
    itemOrcamento.save()
    itemOrcamento = model_to_dict(itemOrcamento)
    return JsonResponse(itemOrcamento)

@login_required(login_url="/auth-user/login-user")
def createItemOrcamento(request):
    data = json.loads(request.body.decode())
    orcamento = Orcamento.objects.get(pk=data.get("orcamento_id"))
    itemOrcamento = OrcamentoItem()
    itemOrcamento.orcamento = orcamento
    if data.get('descricao'):
        itemOrcamento.descricao = data.get('descricao')
    if data.get('tipo'):
        itemOrcamento.tipo = data.get('tipo')
    if data.get('quantidade'):
        itemOrcamento.quantidade = data.get('quantidade')
    if data.get('unidade'):
        itemOrcamento.unidade = data.get('unidade')
    if data.get('valor'):
        itemOrcamento.valor = data.get('valor')
    if 'em_estoque' in data:
        itemOrcamento.em_estoque = data.get('em_estoque')
    if data.get('valor_total'):
        itemOrcamento.valor_total = data.get('valor_total')
    itemOrcamento.save()
    itemOrcamento = model_to_dict(itemOrcamento)
    return JsonResponse(itemOrcamento)

@login_required(login_url="/auth-user/login-user")
def removeItemOrcamento(request, pk):
    itemOrcamento = OrcamentoItem.objects.get(pk=pk)
    itemOrcamento.delete()
    return JsonResponse({"message": "Atividade removida com sucesso!"})

@login_required(login_url="/auth-user/login-user")
def itemOrcamentoForm(request):
    model_id = request.GET.get("model_id")
    context = {}
    if model_id:
        try:
            atividade = OrcamentoItem.objects.get(pk=model_id)
            context["itemOrcamento"] = atividade
        except ObjectDoesNotExist:
            return JsonResponse({"message": "Item de orcamento não encontrado"}, status=400)
    return render(request, 'projetosCotec/itemOrcamentoForm.html', context)

@login_required(login_url="/auth-user/login-user")
def orcamentoTable(request):
    model_id = request.GET.get("model_id")
    context = {}
    if model_id:
        try:
            atividade = Orcamento.objects.get(pk=model_id)
            context["orcamento"] = atividade
        except ObjectDoesNotExist:
            return JsonResponse({"message": "Oramento não encontrado"}, status=400)
    return render(request, 'orcamentos/orcamentoTable.html', context)

# def deleteAll():
#     with transaction.atomic():
#         propostas_projeto = PropostaProjeto.objects.all()
#         print("propostas: ", propostas_projeto)
#         for proposta_projeto in propostas_projeto:
#             print("proposta: ", proposta_projeto)
#             atividades = Atividade.objects.filter(proposta_projeto=proposta_projeto)
#             print("atividades: ", atividades)
#             for atividade in atividades:
#                 atividade.delete()
#                 print("atividade deletada")

#             equipe = MembroExecucao.objects.filter(proposta_projeto=proposta_projeto)
#             print("equipe: ", equipe)
#             for membro in equipe:
#                 membro.delete()
#                 print("membro deletado")

#             orcamento = Orcamento.objects.get(pk=proposta_projeto.orcamento.id)
#             print("orcamento: ", orcamento)
#             orcamento.delete()
#             print("orcamento deletado")
#             proposta_projeto.delete()
#             print("proposta deletada")
    # print(terminou)


@login_required(login_url="/auth-user/login-user")
def createProjetoFromProposta(request, pk):
    with transaction.atomic():
        proposta_projeto = PropostaProjeto.objects.get(pk=pk)
        try:
            evento = proposta_projeto.evento
            return JsonResponse({"message": "Projeto já criado!"}, status=400)
        except ObjectDoesNotExist:
            escola = Escola.objects.get(pk=proposta_projeto.escola.id)
            proposta_projeto = proposta_projeto
            tipo = proposta_projeto.titulo_projeto
            descricao = proposta_projeto.resumo_proposta
            evento = DpEvento.objects.create(
                escola=escola,
                proposta_projeto=proposta_projeto,
                tipo=tipo,
                descricao=descricao,
            )

            eventoEscola = DpEventoEscola.objects.create(escola=escola, dp_evento=evento) 
            eventoEscola.save()
            atividadeSection = AtividadeSection()
            atividadeSection.nome = "Cronograma de Atividades"
            atividadeSection.order = 1
            atividadeSection.evento = evento
            atividadeSection.save()

            atividade_categoria_slug = "tarefa"
            atividade_categoria = AtividadeCategoria.objects.get(slug=atividade_categoria_slug)
            atividades = Atividade.objects.filter(proposta_projeto=proposta_projeto)
            for atividade in atividades:
                atividade.evento = evento
                atividade.atividadeSection = atividadeSection
                atividade.status = "pendente"
                atividade.atividadeCategorias.set([atividade_categoria.id])
                atividade.save()
            
            equipe = MembroExecucao.objects.filter(proposta_projeto=proposta_projeto)
            for membro in equipe:
                membro.evento = evento
                membro.save()
            galeria = Galeria.objects.create(nome="galeria geral do evento ", evento=evento) 
        proposta_projeto.status = "aprovada"
        proposta_projeto.save()
    return JsonResponse({"message": "Projeto criado com sucesso!"})