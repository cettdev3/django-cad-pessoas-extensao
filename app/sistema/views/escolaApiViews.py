# todo/todo_api/views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions
from ..serializers.escolaSerializer import EscolaSerializer
from ..models.escola import Escola
from ..models.dpEvento import DpEvento
from ..models.endereco import Endereco
from ..models.cidade import Cidade
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from django.db import transaction 

class EscolaApiView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    def get_object(self, fn, object_id):
        try:
            return fn.objects.get(id=object_id)
        except fn.DoesNotExist:
            return None

    def get(self, request, *args, **kwargs):
        escolas = None
        evento_id = request.data.get('evento_id')
        if evento_id:
            escolas = DpEvento.objects.get(id=evento_id).escolas.all()
        else: 
            escolas = Escola.objects.all()
        serializer = EscolaSerializer(escolas, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        with transaction.atomic():
            bairro = request.data.get("bairro") 
            logradouro = request.data.get("logradouro") 
            cep = request.data.get("cep") 
            complemento = request.data.get("complemento") 
            cidade = Cidade.objects.get(id = request.data.get("cidade_id"))
            id_siga = request.data.get("id_siga") if request.data.get("id_siga") else None

            nome = request.data.get("nome")
            escola = Escola.objects.create(
                nome = nome,
                cidade = cidade,
                bairro = bairro,
                logradouro = logradouro,
                cep = cep,
                complemento = complemento,
                id_siga = id_siga
            )

            serializer = EscolaSerializer(escola)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

class EscolaDetailApiView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    
    def get_object(self, fn, object_id):
        try:
            return fn.objects.get(id=object_id)
        except fn.DoesNotExist:
            return None
            
    def get(self, request, escola_id, *args, **kwargs):

        escola = self.get_object(escola_id)
        if not escola:
            return Response(
                {"res": "Não existe escola com o id informado"},
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = EscolaSerializer(escola)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, escola_id, *args, **kwargs):
        escola = self.get_object(Escola, escola_id)
        if not escola:
            return Response(
                {"res": "Não existe escola com o id informado"}, 
                status=status.HTTP_400_BAD_REQUEST
            )

        if request.data.get("nome"):
            escola.nome = request.data.get("nome")
        if request.data.get("bairro"):
            escola.bairro = request.data.get("bairro")
        if request.data.get("logradouro"): 
            escola.logradouro = request.data.get("logradouro") 
        if request.data.get("cep"):
            escola.cep = request.data.get("cep") 
        if request.data.get("complemento"):
            escola.complemento = request.data.get("complemento") 
        if request.data.get("cidade_id"):
            escola.cidade = Cidade.objects.get(id = request.data.get("cidade_id"))
        if request.data.get("id_siga"):
            escola.id_siga = request.data.get("id_siga")
        
        escola.save()
        serializer = EscolaSerializer(escola)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, escola_id, *args, **kwargs):
        
        escola = self.get_object(escola_id)
        if not escola:
            return Response(
                {"res": "Não existe escola com o id informado"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        escola.delete()
        return Response(
            {"res": "escola deletada!"},
            status=status.HTTP_200_OK
        )