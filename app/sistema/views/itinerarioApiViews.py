# todo/todo_api/views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions
from ..serializers.itinerarioSerializer import ItinerarioSerializer
from ..models.escola import Escola
from ..models.itinerario import Itinerario
from ..models.itinerarioItem import ItinerarioItem
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
        itinerarios = Itinerario.objects.all()
        serializer = ItinerarioSerializer(itinerarios, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        itinerarioData = {
            "color": request.data.get("color"),
        }

        itinerario = Itinerario.objects.create(**itinerarioData)
        serializer = ItinerarioSerializer(itinerario)
        return Response(serializer.data, status=status.HTTP_200_OK)

class ItinerarioDetailApiView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    
    def get_object(self, fn, object_id):
        try:
            return fn.objects.get(id=object_id)
        except fn.DoesNotExist:
            return None
            
    def get(self, request, itinerario_id, *args, **kwargs):

        itinerario = self.get_object(Itinerario, itinerario_id)
        if not itinerario:
            return Response(
                {"res": "Não existe itinerario com o id informado"},
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = ItinerarioSerializer(itinerario)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, itinerario_id, *args, **kwargs):
        itinerario = self.get_object(Itinerario, itinerario_id)
        if not itinerario:
            return Response(
                {"res": "Não existe itinerario com o id informado"}, 
                status=status.HTTP_400_BAD_REQUEST
            )

        if request.data.get("color"):
            itinerario.nome = request.data.get("color")
        
        itinerario.save()
        serializer = ItinerarioSerializer(itinerario)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, itinerario_id, *args, **kwargs):
        
        itinerario = self.get_object(Itinerario, itinerario_id)
        if not itinerario:
            return Response(
                {"res": "Não existe itinerario com o id informado"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        with transaction.atomic():
            itinerarioItems = ItinerarioItem.objects.filter(itinerario=itinerario)
            for itinerarioItem in itinerarioItems:
                itinerarioItem.delete()
            
            itinerario.delete()
            return Response(
                {"res": "itinerario deletada!"},
                status=status.HTTP_200_OK
            )
        