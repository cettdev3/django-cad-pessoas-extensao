# todo/todo_api/views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions

from ..models.curso import Curso
from ..serializers.cursoSerializer import CursoSerializer
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
class CursoApiView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def get(self, request, *args, **kwargs):
        cursos = Curso.objects.all()
        serializer = CursoSerializer(cursos, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        data = {
            "nome": request.data.get("nome"),
        }

        serializer = CursoSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CursoDetailApiView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    
    def get_object(self, fn, object_id):
        try:
            return fn.objects.get(id=object_id)
        except fn.DoesNotExist:
            return None
            
    def get(self, request, curso_id, *args, **kwargs):

        curso = self.get_object(Curso, curso_id)
        if not curso:
            return Response(
                {"res": "Não existe curso com o id informado"},
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = CursoSerializer(curso)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, curso_id, *args, **kwargs):

        curso = self.get_object(Curso, curso_id)
        if not curso:
            return Response(
                {"res": "Não existe curso com o id informado"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        data = {}
        if request.data.get("nome"):
            data["nome"] = request.data.get("nome")

        serializer = CursoSerializer(instance = curso, data=data, partial = True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, curso_id, *args, **kwargs):
        
        curso = self.get_object(Curso, curso_id)
        if not curso:
            return Response(
                {"res": "Não existe curso com o id informado"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        curso.delete()
        return Response(
            {"res": "curso deletado!"},
            status=status.HTTP_200_OK
        )