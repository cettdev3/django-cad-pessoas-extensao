# todo/todo_api/views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions

from ..models.comentario import Comentario
from ..models.pessoa import Pessoas
from ..models.propostaProjeto import PropostaProjeto
from ..serializers.comentarioSerializer import ComentarioSerializer
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.utils import timezone
from datetime import datetime

class ComentarioApiView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication, JWTAuthentication]

    def get(self, request, *args, **kwargs):
        order_by = request.GET.get('order_by') if request.GET.get('order_by') != "None" else 'created_at'
        comentarios = Comentario.objects
        if order_by:
            comentarios = comentarios.order_by(order_by)
        comentarios = comentarios.all()
        serializer = ComentarioSerializer(comentarios, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        user = request.user
        pessoa = Pessoas.objects.get(user=user)
        if not pessoa:
            return Response(
                {"res": "Não existe pessoa com o id informado"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        proposta_projeto_id = request.data.get("proposta_projeto_id")
        if not proposta_projeto_id:
            return Response(
                {"res": "É necessário informar o id da proposta_projeto"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        proposta_projeto = PropostaProjeto.objects.get(id=proposta_projeto_id)
        if not proposta_projeto:
            return Response(
                {"res": "Não existe proposta_projeto com o id informado"}, 
                status=status.HTTP_400_BAD_REQUEST
            )

        comentario = Comentario.objects.create(
            conteudo=request.data.get("conteudo"),
            autor=pessoa,
            proposta_projeto=proposta_projeto
        )

        serializer = ComentarioSerializer(comentario)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class ComentarioDetailApiView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    
    def get_object(self, fn, object_id):
        try:
            return fn.objects.get(id=object_id)
        except fn.DoesNotExist:
            return None
            
    def get(self, request, comentario_id, *args, **kwargs):

        comentario = self.get_object(Comentario, comentario_id)
        if not comentario:
            return Response(
                {"res": "Não existe comentario com o id informado"},
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = ComentarioSerializer(comentario)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, comentario_id, *args, **kwargs):

        comentario = self.get_object(Comentario, comentario_id)
        if not comentario:
            return Response(
                {"res": "Não existe comentario com o id informado"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        if request.data.get("conteudo"):
            comentario.conteudo = request.data.get("conteudo")
        if request.data.get("autor_id"):
            autor = Pessoas.objects.get(id=request.data.get("autor_id"))
            if not autor:
                return Response(
                    {"res": "Não existe autor com o id informado"}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
            comentario.autor = autor
        
        if request.data.get("proposta_projeto_id"):
            proposta_projeto = PropostaProjeto.objects.get(id=request.data.get("proposta_projeto_id"))
            if not proposta_projeto:
                return Response(
                    {"res": "Não existe proposta_projeto com o id informado"}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
            comentario.proposta_projeto = proposta_projeto
        comentario.save()
        serializer = ComentarioSerializer(comentario)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, comentario_id, *args, **kwargs):
        
        comentario = self.get_object(Comentario, comentario_id)
        if not comentario:
            return Response(
                {"res": "Não existe comentario com o id informado"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        comentario.delete()
        return Response(
            {"res": "comentario deletado!"},
            status=status.HTTP_200_OK
        )