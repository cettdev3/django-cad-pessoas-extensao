# todo/todo_api/views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions

from ..models.acao import Acao
from ..models.pessoa import Pessoas
from ..models.cidade import Cidade
from ..models.ticket import Ticket
from ..models.itinerario import Itinerario
from ..models.itinerarioItem import ItinerarioItem
from ..serializers.acaoSerializer import AcaoSerializer
from ..serializers.itinerarioItemSerializer import ItinerarioItemSerializer
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

class ItinerarioItemApiView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    
    def get_object(self, fn, object_id):
        try:
            return fn.objects.get(id=object_id)
        except fn.DoesNotExist:
            return None

    def get(self, request, *args, **kwargs):
        itinerarioItem = ItinerarioItem.objects.all()
        serializer = ItinerarioItemSerializer(itinerarioItem, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        print("dados dentro da api antes de salvar: ",request.data)
        cidade = None
        if request.data.get("cidade_id"):
            cidade = self.get_object(Cidade, request.data.get("cidade_id"))
            if not cidade:
                return Response(
                    {"res": "Não existe cidade com o id informado"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
        
        itinerario = None
        if request.data.get("itinerario_id"):
            itinerario = self.get_object(Itinerario, request.data.get("itinerario_id"))
            if not itinerario:
                return Response(
                    {"res": "Não existe itinerario com o id informado"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
        else:
            return Response(
                {"res": "É necessário informar o itinerario_id"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        itinerarioItemData = {
            "data_hora": request.data.get("data") if request.data.get("data") else None,
            "endereco": request.data.get("endereco") if request.data.get("endereco") else None,
            "bairro": request.data.get("bairro") if request.data.get("bairro") else None,
            "logradouro": request.data.get("logradouro") if request.data.get("logradouro") else None,
            "cep": request.data.get("cep") if request.data.get("cep") else None,
            "complemento": request.data.get("complemento") if request.data.get("complemento") else None,
            "escola": request.data.get("escola") if request.data.get("escola") else None,
            "latitude": request.data.get("latitude") if request.data.get("latitude") else None,
            "longitude": request.data.get("longitude") if request.data.get("longitude") else None,
            "itinerario": itinerario,
            "cidade": cidade,
        }

        itinerarioItem = ItinerarioItem.objects.create(**itinerarioItemData)
        serializer = ItinerarioItemSerializer(itinerarioItem)
        
        return Response(serializer.data, status=status.HTTP_200_OK)

class ItinerarioItemDetailApiView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    
    def get_object(self, fn, object_id):
        try:
            return fn.objects.get(id=object_id)
        except fn.DoesNotExist:
            return None
            
    def get(self, request, itinerario_item_id, *args, **kwargs):
        itinerarioItem = self.get_object(ItinerarioItem, itinerario_item_id)
        if not itinerarioItem:
            return Response(
                {"res": "Não existe item de itinerario de execução com o id informado"},
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = ItinerarioItemSerializer(itinerarioItem)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, itinerario_item_id, *args, **kwargs):
        itinerarioItem = self.get_object(ItinerarioItem, itinerario_item_id)
        if not itinerarioItem:
            return Response(
                {"res": "Não existe item de ite de execução com o id informado"}, 
                status=status.HTTP_400_BAD_REQUEST
            )

        if request.data.get("data_inicio"):
            itinerarioItem.data_fim = request.data.get("data_inicio")
        if request.data.get("data_hora"):
            itinerarioItem.data_hora = request.data.get("data_hora")
        if request.data.get("endereco"):
            itinerarioItem.endereco = request.data.get("endereco")
        if request.data.get("bairro"):
            itinerarioItem.bairro = request.data.get("bairro")
        if request.data.get("logradouro"):
            itinerarioItem.logradouro = request.data.get("logradouro")
        if request.data.get("cep"):
            itinerarioItem.cep = request.data.get("cep")
        if request.data.get("complemento"):
            itinerarioItem.complemento = request.data.get("complemento")
        if request.data.get("escola"):
            itinerarioItem.escola = request.data.get("escola")
        if request.data.get("latitude"):
            itinerarioItem.latitude = request.data.get("latitude")
        if request.data.get("longitude"):
            itinerarioItem.longitude = request.data.get("longitude")
        if request.data.get("itinerario_id"):
            itinerario = self.get_object(Itinerario, request.data.get("itinerario_id"))
            if not itinerario:
                return Response(
                    {"res": "Não existe itinerario com o id informado"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            itinerarioItem.itinerario = itinerario

        if request.data.get("cidade_id"):
            cidade = self.get_object(Cidade, request.data.get("cidade_id"))
            if not cidade:
                return Response(
                    {"res": "Não existe cidade com o id informado"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            itinerarioItem.cidade = cidade
        
        itinerarioItem.save()
        serializer = ItinerarioItemSerializer(itinerarioItem)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, itinerario_item_id, *args, **kwargs):
        print("itinerario_item_id dentro da: ", itinerario_item_id)
        itinerarioItem = self.get_object(ItinerarioItem, itinerario_item_id)
        if not itinerarioItem:
            return Response(
                {"res": "Não existe item de itinerario com o id informado"}, 
                status=status.HTTP_400_BAD_REQUEST
            )

        itinerarioItem.delete()
        return Response(
            {"res": "itinerario deletado!"},
            status=status.HTTP_200_OK
        )