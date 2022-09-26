# todo/todo_api/views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions
from ..models.pessoa import Pessoas
from ..serializers.pessoaSerializer import PessoaSerializer

class PessoaApiView(APIView):
    # add permission to check if user is authenticated
    permission_classes = [permissions.AllowAny]

    # 1. List all
    def get(self, request, *args, **kwargs):
        todos = Pessoas.objects.all()
        print("dados retornados",todos)
        serializer = PessoaSerializer(todos, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # # 2. Create
    # def post(self, request, *args, **kwargs):
    #     data = {
    #         'nome': request.data.get('nome'), 
    #         'email': request.data.get('email'), 
    #     }
    #     serializer = PessoaSerializer(data=data)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(serializer.data, status=status.HTTP_201_CREATED)

    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)