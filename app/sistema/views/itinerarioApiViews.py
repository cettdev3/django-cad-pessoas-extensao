# todo/todo_api/views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions
from ..serializers.itinerarioSerializer import ItinerarioSerializer
from ..models.escola import Escola
from ..models.itinerario import Itinerario
from ..models.cidade import Cidade
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from django.db import transaction 

class ItinerarioApiView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    
    def get_object(self, fn, object_id):
        try:
            return fn.objects.get(id=object_id)
        except fn.DoesNotExist:
            return None

    def get(self, request, *args, **kwargs):
        print("dentro de get itinerarios")
        itinerarios = Itinerario.objects.all()
        serializer = ItinerarioSerializer(itinerarios, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        with transaction.atomic():
            data = request.data.get 
            print(data)
            # serializer = EscolaSerializer(escola)
            return Response({}, status=status.HTTP_201_CREATED)

class ItinerarioDetailApiView(APIView):
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