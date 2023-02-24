# todo/todo_api/views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions

from ..models.servico import Servico
from ..models.atividade import Atividade
from ..serializers.servicoSerializer import ServicoSerializer
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

class ServicoApiView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def get_object(self, fn, object_id):
        try:
            return fn.objects.get(id=object_id)
        except fn.DoesNotExist:
            return None
        
    def get(self, request, *args, **kwargs):
        cidades = Servico.objects.all()
        serializer = ServicoSerializer(cidades, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        atividade = None
        if request.data.get("atividade_id"):
            atividade = Atividade.objects.get(id=request.data.get("atividade_id"))
            if not atividade:
                return Response(
                    {"res": "Não existe atividade com o id informado"},
                    status=status.HTTP_400_BAD_REQUEST
                )
        else:
            return Response(
                {"res": "O campo atividade_id é obrigatório"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        data = {
            "nome": request.data.get("nome"),
            "quantidadeAtendimentos": request.data.get("quantidadeAtendimentos"),
            "quantidadeVendas": request.data.get("quantidadeVendas"),
            "atividade": atividade,
        }
        
        servico = Servico.objects.create(**data)
        serializer = ServicoSerializer(servico)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class ServicoDetailApiView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    
    def get_object(self, fn, object_id):
        try:
            return fn.objects.get(id=object_id)
        except fn.DoesNotExist:
            return None
            
    def get(self, request, servico_id, *args, **kwargs):

        servico = self.get_object(servico_id)
        if not servico:
            return Response(
                {"res": "Não existe servico com o id informado"},
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = ServicoSerializer(servico)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, servico_id, *args, **kwargs):

        servico = self.get_object(servico_id)
        if not servico:
            return Response(
                {"res": "Não existe servico com o id informado"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        if request.data.get("nome"):
            servico.nome = request.data.get("nome")
        if request.data.get("quantidadeAtendimentos"):
            servico.quantidadeAtendimentos = request.data.get("quantidadeAtendimentos")
        if request.data.get("quantidadeVendas"):
            servico.quantidadeVendas = request.data.get("quantidadeVendas")
        if request.data.get("atividade_id"):
            atividade = Atividade.objects.get(id=request.data.get("atividade_id"))
            if not atividade:
                return Response(
                    {"res": "Não existe atividade com o id informado"},
                    status=status.HTTP_400_BAD_REQUEST
                )
            servico.atividade = atividade

        serializer = ServicoSerializer(servico)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, servico_id, *args, **kwargs):
        
        servico = self.get_object(servico_id)
        if not servico:
            return Response(
                {"res": "Não existe serviço com o id informado"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        servico.delete()
        return Response(
            {"res": "serviço deletada!"},
            status=status.HTTP_200_OK
        )