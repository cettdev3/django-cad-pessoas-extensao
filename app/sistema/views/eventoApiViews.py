# todo/todo_api/views.py
from datetime import datetime
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions

from ..models.endereco import Endereco
from ..models.evento import Evento
from ..serializers.eventoSerializer import EventoSerializer

class EventoApiView(APIView):
    permission_classes = [permissions.AllowAny]
    def get_object(self, fn, object_id):
        try:
            return fn.objects.get(id=object_id)
        except fn.DoesNotExist:
            return None

    def get(self, request, *args, **kwargs):
        eventos = Evento.objects.all()
        print("dados em eventos",eventos)
        serializer = EventoSerializer(eventos, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        data_inicio = None
        data_fim = None
        if request.data.get("data_inicio"):
            data_inicio = datetime.strptime(request.data.get("data_inicio"), "%d-%m-%Y %H:%M:%S")
        if request.data.get("data_fim"):
            data_fim = datetime.strptime(request.data.get("data_fim"), "%d-%m-%Y %H:%M:%S")
        observacao = request.data.get("observacao")
        endereco = self.get_object(Endereco, request.data.get("endereco_id"))

        if not endereco:
            return Response(
                {"res": "Não existe endereco com o id informado"},
                status=status.HTTP_400_BAD_REQUEST
            )

        evento = Evento.objects.create(
            data_inicio = data_inicio,
            data_fim = data_fim,
            observacao = observacao,
            endereco = endereco
        )

        eventoSerializer = EventoSerializer(evento)
        return Response(eventoSerializer.data, status=status.HTTP_201_CREATED)

class EventoDetailApiView(APIView):
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
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = EventoSerializer(evento)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, evento_id, *args, **kwargs):

        evento = self.get_object(Evento, evento_id)
        if not evento:
            return Response(
                {"res": "Não existe evento com o id informado"}, 
                status=status.HTTP_400_BAD_REQUEST
            )

        if request.data.get("data_inicio"):
            evento.data_inicio = datetime.strptime(request.data.get("data_inicio"), "%d-%m-%Y %H:%M:%S")
        if request.data.get("data_fim"):
            evento.data_fim = datetime.strptime(request.data.get("data_fim"), "%d-%m-%Y %H:%M:%S")
        if request.data.get("observacao"):
            evento.observacao = request.data.get("observacao")
        if request.data.get("endereco_id"):
            endereco = self.get_object(Endereco, request.data.get("endereco_id"))
            if not endereco:
                return Response(
                    {"res": "Não existe endereco com o id informado"}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
            evento.endereco = endereco
        evento.save()
        serializer = EventoSerializer(evento)
        
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, evento_id, *args, **kwargs):
        
        evento = self.get_object(Evento, evento_id)
        if not evento:
            return Response(
                {"res": "Não existe evento com o id informado"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        evento.delete()
        return Response(
            {"res": "evento deletada!"},
            status=status.HTTP_200_OK
        )