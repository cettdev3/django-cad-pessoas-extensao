# todo/todo_api/views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions

from ..models.acao import Acao
from ..models.pessoa import Pessoas
from ..models.cidade import Cidade
from ..models.membroExecucao import MembroExecucao
from ..serializers.acaoSerializer import AcaoSerializer
from ..serializers.membroExecucaoSerializer import MembroExecucaoSerializer
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

class MembroExecucaoApiView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    
    def get_object(self, fn, object_id):
        try:
            return fn.objects.get(id=object_id)
        except fn.DoesNotExist:
            return None

    def get(self, request, *args, **kwargs):
        membrosExecucao = MembroExecucao.objects.all()
        serializer = MembroExecucaoSerializer(membrosExecucao, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        cidade = None
        if request.data.get("cidade_id"):
            cidade = self.get_object(Cidade, request.data.get("cidade_id"))
            if not cidade:
                return Response(
                    {"res": "Não existe cidade com o id informado"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
        
        pessoa = None
        if request.data.get("pessoa_id"):
            pessoa = self.get_object(Pessoas, request.data.get("pessoa_id"))
            if not pessoa:
                return Response(
                    {"res": "Não existe pessoa com o id informado"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
        else:
            return Response(
                {"res": "Informe o id da pessoa"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        
        acao = None
        if request.data.get("acao_id"):
            acao = self.get_object(Acao, request.data.get("acao_id"))
            if not acao:
                return Response(
                    {"res": "Não existe acao com o id informado"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
        else:
            return Response(
                {"res": "É necessário informar a ação"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        data = {
            "data_inicio": request.data.get("data_inicio") if request.data.get("data_inicio") else None,
            "data_fim": request.data.get("data_fim") if request.data.get("data_fim") else None,
            "bairro": request.data.get("bairro") if request.data.get("bairro") else None,
            "logradouro": request.data.get("logradouro") if request.data.get("logradouro") else None,
            "cep": request.data.get("cep") if request.data.get("cep") else None,
            "complemento": request.data.get("complemento") if request.data.get("complemento") else None,
            "tipo": request.data.get("tipo") if request.data.get("tipo") else None,
            "cidade": cidade,
            "pessoa": pessoa,
            "acao": acao,
        }

        membroExecucao = MembroExecucao.objects.create(**data)
        serializer = MembroExecucaoSerializer(membroExecucao)
        
        return Response(serializer.data, status=status.HTTP_200_OK)

class MembroExecucaoDetailApiView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    
    def get_object(self, fn, object_id):
        try:
            return fn.objects.get(id=object_id)
        except fn.DoesNotExist:
            return None
            
    def get(self, request, membro_execucao_id, *args, **kwargs):
        memebroExecucao = self.get_object(membro_execucao_id)
        if not memebroExecucao:
            return Response(
                {"res": "Não existe membro da equipe de execução com o id informado"},
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = AcaoSerializer(memebroExecucao)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, membro_execucao_id, *args, **kwargs):
        membroExecucao = self.get_object(MembroExecucao, membro_execucao_id)
        if not membroExecucao:
            return Response(
                {"res": "Não existe membro da equipe de execução com o id informado"}, 
                status=status.HTTP_400_BAD_REQUEST
            )

        if request.data.get("data_inicio"):
            membroExecucao.data_fim = request.data.get("data_inicio")
        if request.data.get("data_fim"):
            membroExecucao.data_fim = request.data.get("data_fim")
        if request.data.get("bairro"):
            membroExecucao.bairro = request.data.get("bairro")
        if request.data.get("logradouro"):
            membroExecucao.logradouro = request.data.get("logradouro")
        if request.data.get("tipo"):
            membroExecucao.tipo = request.data.get("tipo")
        if request.data.get("cep"):
            membroExecucao.cep = request.data.get("cep")
        if request.data.get("complemento"):
            membroExecucao.complemento = request.data.get("complemento")
        if request.data.get("cidade_id"):
            cidade = self.get_object(Cidade, request.data.get("cidade_id"))
            if not cidade:
                return Response(
                    {"res": "Não existe cidade com o id informado"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            membroExecucao.cidade = cidade

        if request.data.get("pessoa_id"):
            pessoa = self.get_object(Pessoas, request.data.get("pessoa_id"))
            if not pessoa:
                return Response(
                    {"res": "Não existe pessoa com o id informado"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            membroExecucao.pessoa = pessoa

        if request.data.get("acao_id"):
            acao = self.get_object(Pessoas, request.data.get("acao_id"))
            if not acao:
                return Response(
                    {"res": "Não existe ação com o id informado"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            membroExecucao.acao = acao

        membroExecucao.save()
        serializer = AcaoSerializer(membroExecucao)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, membro_execucao_id, *args, **kwargs):
        
        membroExecucao = self.get_object(MembroExecucao, membro_execucao_id)
        if not membroExecucao:
            return Response(
                {"res": "Não existe membro da equipe de execução com o id informado"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        membroExecucao.delete()
        return Response(
            {"res": "membro da equipe de execução deletada!"},
            status=status.HTTP_200_OK
        )