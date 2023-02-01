from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions

from ..models.departamento import Departamento
from ..serializers.departamentoSerializer import DepartamentoSerializer
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

class DepartamentoApiView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def get(self, request, *args, **kwargs):
        departamentos = Departamento.objects.all()
        serializer = DepartamentoSerializer(departamentos, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        data = {
            "nome": request.data.get("nome"),
        }
        
        serializer = DepartamentoSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class DepartamentoDetailApiView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def get_object(self, fn, object_id):
        try:
            return fn.objects.get(id=object_id)
        except fn.DoesNotExist:
            return None
            
    def get(self, request, departamento_id, *args, **kwargs):

        departamento = self.get_object(Departamento, departamento_id)
        if not departamento:
            return Response(
                {"res": "Não existe departamento com o id informado"},
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = DepartamentoSerializer(departamento)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, departamento_id, *args, **kwargs):

        departamento = self.get_object(Departamento, departamento_id)
        if not departamento:
            return Response(
                {"res": "Não existe departamento com o id informado"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        data = {}
        if request.data.get("nome"):
            data["nome"] = request.data.get("nome")

        serializer = DepartamentoSerializer(instance = departamento, data=data, partial = True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, departamento_id, *args, **kwargs):
        
        departamento = self.get_object(Departamento, departamento_id)
        if not departamento:
            return Response(
                {"res": "Não existe departamento com o id informado"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        departamento.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)