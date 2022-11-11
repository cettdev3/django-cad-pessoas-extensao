# todo/todo_api/views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions

from ..models.cidade import Cidade
from ..serializers.cidadeSerializer import CidadeSerializer
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
class CidadeApiView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def get(self, request, *args, **kwargs):
        cidades = Cidade.objects.all()
        print("dados em cidades",cidades)
        serializer = CidadeSerializer(cidades, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        data = {
            "nome": request.data.get("nome"),
        }

        serializer = CidadeSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CidadeDetailApiView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    
    def get_object(self, cidade_id):
        try:
            return Cidade.objects.get(id=cidade_id)
        except Cidade.DoesNotExist:
            return None
            
    def get(self, request, cidade_id, *args, **kwargs):

        cidade = self.get_object(cidade_id)
        if not cidade:
            return Response(
                {"res": "Não existe cidade com o id informado"},
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = CidadeSerializer(cidade)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, cidade_id, *args, **kwargs):

        cidade = self.get_object(cidade_id)
        if not cidade:
            return Response(
                {"res": "Não existe cidade com o id informado"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        data = {}
        if request.data.get("nome"):
            data["nome"] = request.data.get("nome")

        serializer = CidadeSerializer(instance = cidade, data=data, partial = True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, cidade_id, *args, **kwargs):
        
        cidade = self.get_object(cidade_id)
        if not cidade:
            return Response(
                {"res": "Não existe cidade com o id informado"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        cidade.delete()
        return Response(
            {"res": "cidade deletada!"},
            status=status.HTTP_200_OK
        )