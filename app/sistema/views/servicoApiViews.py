# todo/todo_api/views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions

from ..models.servico import Servico
from ..models.cidade import Cidade
from ..models.atividade import Atividade
from ..serializers.servicoSerializer import ServicoSerializer
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

class ServicoApiView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication, JWTAuthentication]

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
        cidade = None
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
        if request.data.get("cidade_id"):
            cidade = Cidade.objects.get(id=request.data.get("cidade_id"))
            if not cidade:
                return Response(
                    {"res": "Não existe cidade com o id informado"},
                    status=status.HTTP_400_BAD_REQUEST
                )
        
        data = {
            "nome": request.data.get("nome"),
            "quantidadeAtendimentos": request.data.get("quantidadeAtendimentos") or None,
            "quantidadeVendas": request.data.get("quantidadeVendas") or None,
            "atividade": atividade,
            "cidade": cidade,
            "logradouro": request.data.get("logradouro"),
            "bairro": request.data.get("bairro"),
            "cep": request.data.get("cep"),
            "complemento": request.data.get("complemento"),
            "status": request.data.get("status"),
            "descricao": request.data.get("descricao")
        }
        
        servico = Servico.objects.create(**data)
        serializer = ServicoSerializer(servico)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class ServicoDetailApiView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication, JWTAuthentication]
    
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

        servico = self.get_object(Servico, servico_id)
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
        if request.data.get("cidade_id"):
            cidade = self.get_object(Cidade, request.data.get("cidade_id"))
            if not cidade:
                return Response(
                    {"res": "Não existe cidade com o id informado"},
                    status=status.HTTP_400_BAD_REQUEST
                )
            servico.cidade = cidade
        if request.data.get("logradouro"):
            servico.logradouro = request.data.get("logradouro")
        if request.data.get("bairro"):
            servico.bairro = request.data.get("bairro")
        if request.data.get("cep"):
            servico.cep = request.data.get("cep")
        if request.data.get("complemento"):
            servico.complemento = request.data.get("complemento")
        if request.data.get("status"):
            servico.status = request.data.get("status")
        if request.data.get("descricao"):
            servico.descricao = request.data.get("descricao")

        servico.save()

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