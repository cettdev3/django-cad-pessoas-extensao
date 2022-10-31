# todo/todo_api/views.py
from datetime import datetime
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status as str
from rest_framework import permissions

from ..models.endereco import Endereco
from ..models.evento import Evento
from ..serializers.eventoSerializer import EventoSerializer

class TicketApiView(APIView):
    permission_classes = [permissions.AllowAny]
    def get_object(self, fn, object_id):
        try:
            return fn.objects.get(id=object_id)
        except fn.DoesNotExist:
            return None

    def get(self, request, *args, **kwargs):
        return Response({"res": "rota para resgatar tickets"}, status=str.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        return Response({"res": "rota para criar tickets"}, status=str.HTTP_201_CREATED)    