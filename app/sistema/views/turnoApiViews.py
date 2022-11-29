# todo/todo_api/views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions

from ..models.turno import Turno
from ..serializers.turnoSerializer import TurnoSerializer
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

class TurnoApiView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def get(self, request, *args, **kwargs):
        tunos = Turno.objects.all()
        serializer = TurnoSerializer(tunos, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        data = {
            "nome": request.data.get("nome"),
            "carga_horaria": request.data.get("carga_horaria"),
        }

        serializer = TurnoSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class TurnoDetailApiView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    
    def get_object(self, turno_id):
        try:
            return Turno.objects.get(id=turno_id)
        except Turno.DoesNotExist:
            return None
            
    def get(self, request, turno_id, *args, **kwargs):

        turno = self.get_object(turno_id)
        if not turno:
            return Response(
                {"res": "Não existe turno com o id informado"},
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = TurnoSerializer(turno)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, turno_id, *args, **kwargs):

        turno = self.get_object(turno_id)
        if not turno:
            return Response(
                {"res": "Não existe turno com o id informado"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        data = {}
        if request.data.get("nome"):
            data["nome"] = request.data.get("nome")
        if request.data.get("carga_horaria"):
            data["carga_horaria"] = request.data.get("carga_horaria")

        serializer = TurnoSerializer(instance = turno, data=data, partial = True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, turno_id, *args, **kwargs):
        
        turno = self.get_object(turno_id)
        if not turno:
            return Response(
                {"res": "Não existe turno com o id informado"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        turno.delete()
        return Response(
            {"res": "turno deletada!"},
            status=status.HTTP_200_OK
        )