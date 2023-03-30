# todo/todo_api/views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions

from ..models.dataRemovida import DataRemovida
from ..models.alocacao import Alocacao
from ..serializers.dataRemovidaSerializer import DataRemovidaSerializer
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

class DataRemovidaApiView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def get_object(self, fn, object_id):
        try:
            return fn.objects.get(id=object_id)
        except fn.DoesNotExist:
            return None

    def post(self, request, *args, **kwargs):
        print("requisição : ", request.data)
        alocacao = None
        if request.data.get("alocacao_id"):
            alocacao = self.get_object(Alocacao, request.data.get("alocacao_id"))
            if not alocacao:
                return Response(
                    {"res": "Não existe alocacao com o id informado"},
                    status=status.HTTP_400_BAD_REQUEST
                )

        data = {
            "date": request.data.get("date"),
            "alocacao": alocacao
        }
        
        dataRemovida = DataRemovida.objects.create(**data)
        serializer = DataRemovidaSerializer(dataRemovida)
        return Response(serializer.data, status=status.HTTP_201_CREATED)