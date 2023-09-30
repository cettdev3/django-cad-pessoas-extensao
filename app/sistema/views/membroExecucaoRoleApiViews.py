# todo/todo_api/views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from ..models.membroExecucaoRoles import MembroExecucaoRoles
from ..serializers.membroExecucaoRoleSerializer import MembroExecucaoRoleSerializer
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
import re

def create_slug_from_name(name):
    if not name:
        return None
    
    slug = name.lower()
    
    slug = re.sub(r'[^\w\s]', '', slug)
    
    slug = slug.replace(' ', '_')
    
    return slug

class MembroExecucaoRoleApiView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication, JWTAuthentication]
    
    def get_object(self, fn, object_id):
        try:
            return fn.objects.get(id=object_id)
        except fn.DoesNotExist:
            return None

    def get(self, request, *args, **kwargs):
        slugs = [
            MembroExecucaoRoles.SLUG_PROPONENTE,
            MembroExecucaoRoles.SLUG_RESPONSAVEL,
            MembroExecucaoRoles.SLUG_PRFESSOR
        ]
        membrosExecucaoroles = MembroExecucaoRoles.objects.filter(slug__in=slugs)
        serializer = MembroExecucaoRoleSerializer(membrosExecucaoroles, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs): 
        slug = None 
        if request.data.get("nome"):
            slug = create_slug_from_name(request.data.get("nome"))
        data = {
            "nome": request.data.get("nome"),
            "slug": slug
        }

        membroExecucao = MembroExecucaoRoles.objects.create(**data)
        serializer = MembroExecucaoRoleSerializer(membroExecucao)
        
        return Response(serializer.data, status=status.HTTP_200_OK)

class MembroExecucaoRoleDetailApiView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    
    def get_object(self, fn, object_id):
        try:
            return fn.objects.get(id=object_id)
        except fn.DoesNotExist:
            return None
            
    def get(self, request, membro_execucao_role_id, *args, **kwargs):
        memebroExecucaoRole = MembroExecucaoRoles.objects.get(id=membro_execucao_role_id)
        if not memebroExecucaoRole:
            return Response(
                {"res": "Não existe função da equipe de execução com o id informado"},
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = MembroExecucaoRoleSerializer(memebroExecucaoRole)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, membro_execucao_role_id, *args, **kwargs):
        membroExecucaoRole = self.get_object(MembroExecucaoRoles, membro_execucao_role_id)
        if not membroExecucaoRole:
            return Response(
                {"res": "Não existe função da equipe de execução com o id informado"}, 
                status=status.HTTP_400_BAD_REQUEST
            )

        if request.data.get("nome"):
            membroExecucaoRole.nome = request.data.get("nome")
            membroExecucaoRole.slug = create_slug_from_name(request.data.get("nome"))

        membroExecucaoRole.save()
        serializer = MembroExecucaoRoleSerializer(membroExecucaoRole)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, membro_execucao_role_id, *args, **kwargs):
        membroExecucaoRole = self.get_object(MembroExecucaoRoles, membro_execucao_role_id)
        if not membroExecucaoRole:
            return Response(
                {"res": "Não existe função da equipe de execução com o id informado"}, 
                status=status.HTTP_400_BAD_REQUEST
            )

        membroExecucaoRole.delete()
        return Response(
            {"res": "membro função da equipe de execução deletada!"},
            status=status.HTTP_200_OK
        )
