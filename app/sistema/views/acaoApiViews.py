# todo/todo_api/views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions

from ..models.acao import Acao
from ..models.cidade import Cidade
from ..serializers.acaoSerialyzer import AcaoSerializer
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
        print("cidade id",request.data.get("cidade_id"))
        if request.data.get("cidade_id"):
            cidade = self.get_object(Cidade, request.data.get("cidade_id"))
            if not cidade:
                return Response(
                    {"res": "Não existe cidade com o id informado"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

        data = {
            "tipo": request.data.get("tipo"),
            "descricao": request.data.get("descricao"),
            "data_inicio": request.data.get("data_inicio"),
            "data_fim": request.data.get("data_fim"),
            "bairro": request.data.get("bairro"),
            "logradouro": request.data.get("logradouro"),
            "cep": request.data.get("cep"),
            "complemento": request.data.get("complemento"),
            "cidade": cidade,
        }

        serializer = AcaoSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class AcaoDetailApiView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    
    def get_object(self, acao_id):
        try:
            return Acao.objects.get(id=acao_id)
        except Acao.DoesNotExist:
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
        acao = self.get_object(acao_id)
        if not acao:
            return Response(
                {"res": "Não existe ação com o id informado"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        data = {}
        if request.data.get("tipo"):
            data["tipo"] = request.data.get("tipo")
        if request.data.get("descricao"):
            data["descricao"] = request.data.get("descricao")

        serializer = AcaoSerializer(instance = acao, data=data, partial = True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

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