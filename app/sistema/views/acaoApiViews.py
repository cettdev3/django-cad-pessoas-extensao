# todo/todo_api/views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions

from ..models.acao import Acao
from ..models.cidade import Cidade
from ..serializers.acaoSerializer import AcaoSerializer
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

class AcaoApiView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    
    def get_object(self, fn, object_id):
        try:
            return fn.objects.get(id=object_id)
        except fn.DoesNotExist:
            return None

    def get(self, request, *args, **kwargs):
        acoes = Acao.objects.all()
        serializer = AcaoSerializer(acoes, many=True)
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

        data = {
            "tipo": request.data.get("tipo") if request.data.get("tipo") else None,
            "descricao": request.data.get("descricao") if request.data.get("descricao") else None,
            "data_inicio": request.data.get("data_inicio") if request.data.get("data_inicio") else None,
            "data_fim": request.data.get("data_fim") if request.data.get("data_fim") else None,
            "bairro": request.data.get("bairro") if request.data.get("bairro") else None,
            "logradouro": request.data.get("logradouro") if request.data.get("logradouro") else None,
            "cep": request.data.get("cep") if request.data.get("cep") else None,
            "complemento": request.data.get("complemento") if request.data.get("complemento") else None,
            "cidade": cidade,
        }
        acao = Acao.objects.create(**data)
        serializer = AcaoSerializer(acao)
        
        return Response(serializer.data, status=status.HTTP_200_OK)

class AcaoDetailApiView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    
    def get_object(self, fn, object_id):
        try:
            return fn.objects.get(id=object_id)
        except fn.DoesNotExist:
            return None
            
    def get(self, request, acao_id, *args, **kwargs):

        acao = self.get_object(acao_id)
        if not acao:
            return Response(
                {"res": "Não existe ação com o id informado"},
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = AcaoSerializer(acao)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, acao_id, *args, **kwargs):
        acao = self.get_object(Acao, acao_id)
        if not acao:
            return Response(
                {"res": "Não existe ação com o id informado"}, 
                status=status.HTTP_400_BAD_REQUEST
            )

        if request.data.get("tipo"):
            acao.tipo = request.data.get("tipo")
        if request.data.get("descricao"):
            acao.descricao = request.data.get("descricao")
        if request.data.get("data_inicio"):
            acao.data_inicio = request.data.get("data_inicio")
        if request.data.get("data_fim"):
            acao.data_fim = request.data.get("data_fim")
        if request.data.get("bairro"):
            acao.bairro = request.data.get("bairro")
        if request.data.get("logradouro"):
            acao.logradouro = request.data.get("logradouro")
        if request.data.get("cep"):
            acao.cep = request.data.get("cep")
        if request.data.get("complemento"):
            acao.complemento = request.data.get("complemento")
        if request.data.get("cidade_id"):
            cidade = self.get_object(Cidade, request.data.get("cidade_id"))
            if not cidade:
                return Response(
                    {"res": "Não existe cidade com o id informado"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            acao.cidade = cidade

        acao.save()
        serializer = AcaoSerializer(acao)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, acao_id, *args, **kwargs):
        
        acao = self.get_object(acao_id)
        if not acao:
            return Response(
                {"res": "Não existe ação com o id informado"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        acao.delete()
        return Response(
            {"res": "ação deletada!"},
            status=status.HTTP_200_OK
        )