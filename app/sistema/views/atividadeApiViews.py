# todo/todo_api/views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions
from django.db import transaction

from django.db.models import Prefetch
from ..models.acao import Acao
from ..models.tipoAtividade import TipoAtividade
from ..models.cidade import Cidade
from ..models.atividade import Atividade
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
        atividades = Atividade.objects.select_related("acao", "tipoAtividade", "responsavel", "cidade").all()
        serializer = AtividadeSerializer(atividades, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        acao = None
        tipoAtividade = None
        responsavel = None 
        cidade = None

        data = request.data
        if data["cidade_id"]:
            cidade = self.get_object(Cidade, data["cidade_id"])
            if not cidade:
                return Response(
                    {"res": "Não existe cidade com o id informado"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

        if data["acao_id"]:
            acao = self.get_object(Acao, data["acao_id"])
            if not acao:
                return Response(
                    {"res": "Não existe acao com o id informado"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
        
        if data["tipo_atividade_id"]:
            tipoAtividade = self.get_object(TipoAtividade, data["tipo_atividade_id"])
            if not tipoAtividade:
                return Response(
                    {"res": "Não existe tipo de atividade com o id informado"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
        
        if data["membro_execucao_id"]:
            responsavel = self.get_object(MembroExecucao, data["membro_execucao_id"])
            if not responsavel:
                return Response(
                    {"res": "Não existe responsável com o id informado"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
        
        atividadeData = {
            "descricao": data["descricao"] if data["descricao"] else None,
            "status": data["status"] if data["status"] else "planejado",
            "linkDocumentos": data["linkDocumentos"] if data["linkDocumentos"] else None,
            "acao": acao,
            "tipoAtividade": tipoAtividade,
            "responsavel": responsavel,
            "cidade": cidade,
            "logradouro": data["logradouro"] if data["logradouro"] else None,
            "bairro": data["bairro"] if data["bairro"] else None,
            "cep": data["cep"] if data["cep"] else None,
            "complemento": data["complemento"] if data["complemento"] else None,
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

        atividade = self.get_object(Atividade, atividade_id)
        if not atividade:
            return Response(
                {"res": "Não existe atividade com o id informado"},
                status=status.HTTP_400_BAD_REQUEST
            )

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
        if data["cidade_id"]:
            cidade = self.get_object(Cidade, data["cidade_id"])
            if not cidade:
                return Response(
                    {"res": "Não existe cidade com o id informado"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            atividade.cidade = cidade
        
        if data["acao_id"]:
            acao = self.get_object(Acao, data["acao_id"])
            if not acao:
                return Response(
                    {"res": "Não existe ação com o id informado"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            atividade.acao = acao

        if data["tipo_atividade_id"]:
            tipoAtividade = self.get_object(TipoAtividade, data["tipo_atividade_id"])
            if not tipoAtividade:
                return Response(
                    {"res": "Não existe tipo de atividade com o id informado"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            atividade.tipoAtividade = tipoAtividade
        
        if data["membro_execucao_id"]:
            responsavel = self.get_object(MembroExecucao, data["membro_execucao_id"])
            if not responsavel:
                return Response(
                    {"res": "Não existe responsável com o id informado"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            atividade.responsavel = responsavel
        
        if data["descricao"]:
            atividade.descricao = data["descricao"]
        if data["status"]:
            atividade.status = data["status"]
        if data["linkDocumentos"]:
            atividade.linkDocumentos = data["linkDocumentos"]
        if data["logradouro"]:
            atividade.logradouro = data["logradouro"]
        if data["bairro"]:
            atividade.bairro = data["bairro"]
        if data["cep"]:
            atividade.cep = data["cep"]
        if data["complemento"]:
            atividade.complemento = data["complemento"]

        atividade.save()
        serializer = AtividadeSerializer(acao)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, atividade_id, *args, **kwargs):

        atividade = self.get_object(Atividade, atividade_id)
        if not atividade:
            return Response(
                {"res": "Não existe atividade com o id informado"},
                status=status.HTTP_400_BAD_REQUEST
            )

        atividade.delete()
        return Response(
            {"res": "atividade deletada!"},
            status=status.HTTP_200_OK
        )