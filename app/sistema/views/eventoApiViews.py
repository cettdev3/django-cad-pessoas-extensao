# todo/todo_api/views.py
from datetime import datetime
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status as str
from rest_framework import permissions

from ..models.cidade import Cidade
from ..models.endereco import Endereco
from ..models.evento import Evento
from ..serializers.eventoSerializer import EventoSerializer
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

class EventoApiView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def get_object(self, fn, object_id):
        try:
            return fn.objects.get(id=object_id)
        except fn.DoesNotExist:
            return None

    def get(self, request, *args, **kwargs):
        eventos = Evento.objects.all()
        serializer = EventoSerializer(eventos, many=True)
        return Response(serializer.data, status=str.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        data_inicio = None
        data_fim = None
        if request.data.get("data_inicio"):
            data_inicio = datetime.strptime(request.data.get("data_inicio"), '%Y-%m-%dT%H:%M')
        if request.data.get("data_fim"):
            data_fim = datetime.strptime(request.data.get("data_fim"), '%Y-%m-%dT%H:%M')
        observacao = request.data.get("observacao")
        status = request.data.get("status")
        endereco = None
        if request.data.get("endereco_id"):
            endereco = self.get_object(Endereco, request.data.get("endereco_id"))

            if not endereco:
                return Response(
                    {"res": "Não existe endereco com o id informado"},
                    status=str.HTTP_400_BAD_REQUEST
                )

        evento = Evento.objects.create(
            data_inicio = data_inicio,
            data_fim = data_fim,
            observacao = observacao,
            status = status,
            logradouro = endereco.logradouro if endereco else None,
            complemento = endereco.complemento if endereco else None,
            bairro = endereco.bairro if endereco else None,
            cidade = endereco.cidade if endereco else None,
            cep = endereco.cep if endereco else None,
        )

        eventoSerializer = EventoSerializer(evento)
        return Response(eventoSerializer.data, status=str.HTTP_201_CREATED)

class EventoDetailApiView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    
    def get_object(self, fn, object_id):
        try:
            return fn.objects.get(id=object_id)
        except fn.DoesNotExist:
            return None
            
    def get(self, request, evento_id, *args, **kwargs):

        evento = self.get_object(Evento, evento_id)
        if not evento:
            return Response(
                {"res": "Não existe evento com o id informado"},
                status=str.HTTP_400_BAD_REQUEST
            )

        serializer = EventoSerializer(evento)
        return Response(serializer.data, status=str.HTTP_200_OK)

    def put(self, request, evento_id, *args, **kwargs):

        evento = self.get_object(Evento, evento_id)
        if not evento:
            return Response(
                {"res": "Não existe evento com o id informado"}, 
                status=str.HTTP_400_BAD_REQUEST
            )
        print("valor do cep: ", request.data.get("cep"))
        print("valor do logradouro", request.data.get("logradouro"))
        print("valor do complemento", request.data.get("complemento"))
        print("valor do bairro", request.data.get("bairro"))
        print("valor do cidade", request.data.get("cidade"))

        if request.data.get("data_inicio"):
            evento.data_inicio = datetime.strptime(request.data.get("data_inicio"), '%Y-%m-%dT%H:%M')
        if request.data.get("data_fim"):
            evento.data_fim = datetime.strptime(request.data.get("data_fim"), '%Y-%m-%dT%H:%M')
        if request.data.get("observacao"):
            evento.observacao = request.data.get("observacao")
        if request.data.get("status"):
            evento.status = request.data.get("status")
        if request.data.get("logradouro"):
            evento.logradouro = request.data.get("logradouro")
        if request.data.get("complemento"):
            evento.complemento = request.data.get("complemento")
        if request.data.get("bairro"):
            evento.bairro = request.data.get("bairro")
        if request.data.get("cidade_id"):
            cidade = self.get_object(Cidade, request.data.get("cidade_id"))
            if not cidade:
                return Response(
                    {"res": "Não existe evento com o id informado"}, 
                    status=str.HTTP_400_BAD_REQUEST
                )
            evento.cidade = cidade
        if request.data.get("cep"):
            evento.cep = request.data.get("cep")

        evento.save()
        serializer = EventoSerializer(evento)
        
        return Response(serializer.data, status=str.HTTP_200_OK)

    def delete(self, request, evento_id, *args, **kwargs):
        
        evento = self.get_object(Evento, evento_id)
        if not evento:
            return Response(
                {"res": "Não existe evento com o id informado"}, 
                status=str.HTTP_400_BAD_REQUEST
            )
        evento.delete()
        return Response(
            {"res": "evento deletada!"},
            status=str.HTTP_200_OK
        )