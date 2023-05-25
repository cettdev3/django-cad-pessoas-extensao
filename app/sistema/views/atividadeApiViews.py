# todo/todo_api/views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions
from django.db import transaction

from django.db.models import Prefetch, OuterRef
from ..models.acao import Acao
from ..models.tipoAtividade import TipoAtividade
from ..models.cidade import Cidade
from ..models.atividade import Atividade
from ..models.servico import Servico
from ..models.atividadeSection import AtividadeSection
from ..models.departamento import Departamento
from ..models.dpEvento import DpEvento
from ..models.galeria import Galeria
from ..models.anexo import Anexo
from ..models.membroExecucao import MembroExecucao
from ..serializers.atividadeSerializer import AtividadeSerializer
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from django.db import reset_queries
from datetime import datetime
from django.db import connection

class AtividadeApiView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def get_object(self, fn, object_id):
        try:
            return fn.objects.get(id=object_id)
        except fn.DoesNotExist:
            return None

    def get(self, request, *args, **kwargs):
        atividades = Atividade.objects.select_related(
            "acao", 
            "tipoAtividade", 
            "departamento", 
            "responsavel",
            "cidade",
        ).prefetch_related("servico_set", "ticket_set").all()

        atividades = atividades.prefetch_related(Prefetch(
            'anexo_set',
            queryset=Anexo.objects.filter(model='Atividade', id_model=OuterRef('pk')),
            to_attr='anexos'
        ))

        serializer = AtividadeSerializer(atividades, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        acao = None
        tipoAtividade = None
        responsavel = None 
        cidade = None
        evento = None
        departamento = None
        section = None

        data = request.data
        if data.get("cidade_id"):
            cidade = self.get_object(Cidade, data["cidade_id"])
            if not cidade:
                return Response(
                    {"res": "Não existe cidade com o id informado"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

        if data.get("acao_id"):
            acao = self.get_object(Acao, data["acao_id"])
            if not acao:
                return Response(
                    {"res": "Não existe acao com o id informado"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
        
        if data.get("evento_id"):
            evento = self.get_object(DpEvento, data["evento_id"])
            if not evento:
                return Response(
                    {"res": "Não existe evento com o id informado"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
        
        if data.get("tipo_atividade_id"):
            tipoAtividade = self.get_object(TipoAtividade, data["tipo_atividade_id"])
            if not tipoAtividade:
                return Response(
                    {"res": "Não existe tipo de atividade com o id informado"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
        
        if data.get("membro_execucao_id"):
            responsavel = self.get_object(MembroExecucao, data["membro_execucao_id"])
            if not responsavel:
                return Response(
                    {"res": "Não existe responsável com o id informado"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
        
        if data.get("departamento_id"):
            departamento = self.get_object(Departamento, data["departamento_id"])
            if not departamento:
                return Response(
                    {"res": "Não existe departamento com o id informado"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            
        if data.get("atividade_section_id"):
            section = self.get_object(AtividadeSection, data["atividade_section_id"])
            if not section:
                return Response(
                    {"res": "Não existe seção com o id informado"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            
        categoria = data.get("categoria", "tarefa")
        atividade_meta = False
        if categoria == 'meta_extensao':
            atividade_meta = True

        galeria = Galeria.objects.create(nome="Galeria sem titulo ", evento=evento)
        atividadeData = {
            "descricao": data.get("descricao"),
            "quantidadeCertificacoes": data.get("quantidadeCertificacoes"),
            "quantidadeMatriculas": data.get("quantidadeMatriculas"),
            "quantidadeAtendimentos": data.get("quantidadeAtendimentos"),
            "quantidadeInscricoes": data.get("quantidadeInscricoes"),
            "cargaHoraria": data.get("cargaHoraria"),
            "status": data.get("status", "pendente"),
            "linkDocumentos": data.get("linkDocumentos"),
            "acao": acao,
            "evento": evento,
            "tipoAtividade": tipoAtividade,
            "responsavel": responsavel,
            "departamento": departamento,
            "data_realizacao_inicio": datetime.strptime(data["data_realizacao_inicio"], "%Y-%m-%d").date() if data.get("data_realizacao_inicio") else None,
            "data_realizacao_fim": datetime.strptime(data["data_realizacao_fim"], "%Y-%m-%d").date() if data.get("data_realizacao_fim") else None,
            "cidade": cidade,
            "galeria": galeria,
            "logradouro": data.get("logradouro"),
            "bairro": data.get("bairro"),
            "cep": data.get("cep"),
            "complemento": data.get("complemento"),
            "valor": float(data["valor"]) if data.get("valor") else None,
            "categoria": data.get("categoria", "tarefa"),
            "atividade_meta": atividade_meta,
            "atividadeSection": section
        }

        atividade = Atividade.objects.create(**atividadeData)
        serializer = AtividadeSerializer(atividade)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class AtividadeDetailApiView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def get_object(self, fn, object_id):
        try:
            return fn.objects.get(id=object_id)
        except fn.DoesNotExist:
            return None

    def get(self, request, atividade_id, *args, **kwargs):
        print("rota de get atividade")
        atividade = Atividade.objects.filter(id=atividade_id)
        atividade = atividade.select_related(
            "acao", 
            "tipoAtividade", 
            "departamento", 
            "responsavel",
            "cidade"
        ).prefetch_related("servico_set", "ticket_set").first()

        if not atividade:
            return Response(
                {"res": "Não existe atividade com o id informado"},
                status=status.HTTP_400_BAD_REQUEST
            )

        anexos = Anexo.objects.filter(model='Atividade', id_model=atividade.id)
        anexos = list(anexos.values())

        atividade.anexos = anexos

        serializer = AtividadeSerializer(atividade)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, atividade_id, *args, **kwargs):
        atividade = self.get_object(Atividade, atividade_id)
        if not atividade:
            return Response(
                {"res": "Não existe atividade com o id informado"},
                status=status.HTTP_400_BAD_REQUEST
            )

        data = request.data
        if data.get("cidade_id"):
            cidade = self.get_object(Cidade, data.get("cidade_id"))
            if not cidade:
                return Response(
                    {"res": "Não existe cidade com o id informado"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            atividade.cidade = cidade

        if data.get("acao_id"):
            acao = self.get_object(Acao, data.get("acao_id"))
            if not acao:
                return Response(
                    {"res": "Não existe ação com o id informado"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            atividade.acao = acao

        if data.get("evento_id"):
            evento = self.get_object(DpEvento, data.get("evento_id"))
            if not evento:
                return Response(
                    {"res": "Não existe evento com o id informado"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            atividade.evento = evento

        if data.get("tipo_atividade_id"):
            tipoAtividade = self.get_object(TipoAtividade, data.get("tipo_atividade_id"))
            if not tipoAtividade:
                return Response(
                    {"res": "Não existe tipo de atividade com o id informado"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            atividade.tipoAtividade = tipoAtividade

        if data.get("membro_execucao_id"):
            responsavel = self.get_object(MembroExecucao, data.get("membro_execucao_id"))
            if not responsavel:
                return Response(
                    {"res": "Não existe responsável com o id informado"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            atividade.responsavel = responsavel

        if data.get("departamento_id"):
            departamento = self.get_object(Departamento, data.get("departamento_id"))
            if not departamento:
                return Response(
                    {"res": "Não existe departamento com o id informado"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            atividade.departamento = departamento

        if data.get("quantidadeCertificacoes") == '':
            atividade.quantidadeCertificacoes = None
        else: 
            atividade.quantidadeCertificacoes = data.get("quantidadeCertificacoes", atividade.quantidadeCertificacoes) 

        if data.get("quantidadeMatriculas") == '':
            atividade.quantidadeMatriculas = None
        else: 
            atividade.quantidadeMatriculas = data.get("quantidadeMatriculas", atividade.quantidadeMatriculas) 

        if data.get("quantidadeAtendimentos") == '':
            atividade.quantidadeAtendimentos = None
        else: 
            atividade.quantidadeAtendimentos = data.get("quantidadeAtendimentos", atividade.quantidadeAtendimentos) 

        if data.get("quantidadeInscricoes") == '':
            atividade.quantidadeInscricoes = None
        else: 
            atividade.quantidadeInscricoes = data.get("quantidadeInscricoes", atividade.quantidadeInscricoes) 

        if data.get("cargaHoraria") == '':
            atividade.cargaHoraria = None
        else: 
            atividade.cargaHoraria = data.get("cargaHoraria", atividade.cargaHoraria) 
        
        if data.get("valor") == '':
            atividade.valor = None
        else:
            atividade.valor = data.get("valor", atividade.valor)

        if data.get("nome"):
            galeriaId = atividade.galeria.id
            galeria = self.get_object(Galeria, galeriaId)
            galeria.nome = data.get("nome")
            galeria.save()
            atividade.nome = data.get("nome", atividade.nome)

        categoria = data.get("categoria", atividade.categoria)
        if categoria == atividade.CATEGORIA_META_EXTENSAO:
            atividade.atividade_meta = True
        else:
            atividade.atividade_meta = False

        atividade.descricao = data.get("descricao", atividade.descricao)
        atividade.status = data.get("status", atividade.status)
        atividade.linkDocumentos = data.get("linkDocumentos", atividade.linkDocumentos)
        atividade.logradouro = data.get("logradouro", atividade.logradouro)
        atividade.bairro = data.get("bairro", atividade.bairro)
        atividade.cep = data.get("cep", atividade.cep)
        atividade.complemento = data.get("complemento", atividade.complemento)
        atividade.data_realizacao_inicio = data.get("data_realizacao_inicio", atividade.data_realizacao_inicio)
        atividade.data_realizacao_fim = data.get("data_realizacao_fim", atividade.data_realizacao_fim)
        atividade.categoria = categoria
        atividade.save()

        anexos = Anexo.objects.filter(model='Atividade', id_model=atividade.id)
        anexos = list(anexos.values())

        atividade.anexos = anexos
        serializer = AtividadeSerializer(atividade)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, atividade_id, *args, **kwargs):

        atividade = self.get_object(Atividade, atividade_id)
        if not atividade:
            return Response(
                {"res": "Não existe atividade com o id informado"},
                status=status.HTTP_400_BAD_REQUEST
            )
        with transaction.atomic():
            anexos = Anexo.objects.filter(model='Atividade', id_model=atividade.id)
            for anexo in anexos:
                anexo.delete()
            
            servicos = Servico.objects.filter(atividade=atividade)
            for servico in servicos:
                servico.delete()

            atividade.delete()
        return Response(
            {"res": "atividade deletada!"},
            status=status.HTTP_200_OK
        )