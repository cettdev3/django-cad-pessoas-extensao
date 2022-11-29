# todo/todo_api/views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions

from ..models.endereco import Endereco
from ..models.cidade import Cidade
from ..serializers.enderecoSerializer import EnderecoSerializer
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
class EnderecoApiView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def get(self, request, *args, **kwargs):
        eventos = Endereco.objects.all()
        serializer = EnderecoSerializer(eventos, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        bairro = request.data.get("bairro") 
        logradouro = request.data.get("logradouro") 
        cep = request.data.get("cep") 
        complemento = request.data.get("complemento") 
        cidade = Cidade.objects.get(id = request.data.get("cidade_id"))
        endereco = Endereco.objects.create(
            cidade = cidade,
            bairro = bairro,
            logradouro = logradouro,
            cep = cep,
            complemento = complemento,
        )

        endereco.save()
        serializer = EnderecoSerializer(endereco)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class EnderecoDetailApiView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    
    def get_object(self, fn, object_id):
        try:
            return fn.objects.get(id=object_id)
        except fn.DoesNotExist:
            return None
            
    def get(self, request, endereco_id, *args, **kwargs):

        endereco = self.get_object(Endereco, endereco_id)
        if not endereco:
            return Response(
                {"res": "Não existe endereco com o id informado"},
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = EnderecoSerializer(endereco)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, endereco_id, *args, **kwargs):
        endereco = self.get_object(Endereco, endereco_id)
        if not endereco:
            return Response(
                {"res": "Não existe endereco com o id informado"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        if request.data.get("bairro"):
            endereco.bairro = request.data.get("bairro")
        if request.data.get("logradouro"):
            endereco.logradouro = request.data.get("logradouro")
        if request.data.get("cep"):
            endereco.cep = request.data.get("cep")
        if request.data.get("complemento"):
            endereco.complemento = request.data.get("complemento")
        if request.data.get("cidade_id"):
            cidade = self.get_object(Cidade, request.data.get("cidade_id"))
            if not cidade:
                return Response(
                    {"res": "Não existe cidade com o id informado"}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
            endereco.cidade = cidade
        endereco.save()

        serializer = EnderecoSerializer(endereco)        
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, endereco_id, *args, **kwargs):
        
        endereco = self.get_object(Endereco, endereco_id)
        if not endereco:
            return Response(
                {"res": "Não existe endereco com o id informado"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        endereco.delete()
        return Response(
            {"res": "endereco deletada!"},
            status=status.HTTP_200_OK
        )