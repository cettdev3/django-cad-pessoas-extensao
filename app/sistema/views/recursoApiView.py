from datetime import datetime
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status as st
from django.db import transaction
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from sistema.models import (
    Recursos,
    PropostaProjeto
)

from sistema.serializers import (
    RecursoSerializer
)
        
class RecursoApiView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def get_object(self, fn, object_id):
            try:
                return fn.objects.get(id=object_id)
            except fn.DoesNotExist:
                return None

    def get(self, request, *args, **kwargs):
        recursos = Recursos.objects.all()
        if request.GET.get("evento_id"):
            recursos = recursos.filter(evento_id=request.GET.get("evento_id"))
        if request.GET.get("proposta_projeto_id"):
            recursos = recursos.filter(proposta_projeto_id=request.GET.get("proposta_projeto_id"))
        serializer = RecursoSerializer(recursos, many=True)
        return Response(serializer.data, status=st.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        proposta_projeto = None
        
        if request.data.get("proposta_projeto_id"):
            proposta_projeto = self.get_object(PropostaProjeto, request.data.get("proposta_projeto_id"))
            if not PropostaProjeto:
                return Response(
                    {"res": "Não existe proposta de projeto com o id informado"}, 
                    status=st.HTTP_400_BAD_REQUEST
                )

        recurso = Recursos.objects.create(
            nome = request.data.get("nome", None),
            descricao = request.data.get("descricao", None),
            quantidade = request.data.get("quantidade", None),
            unidade = request.data.get("unidade", None),
            valor = request.data.get("valor", None),
            valor_total = request.data.get("valor_total", None),
            em_estoque = request.data.get("em_estoque", False),
            proposta_projeto = proposta_projeto
        )

        recursoSerializer = RecursoSerializer(recurso)
        return Response(recursoSerializer.data, status=st.HTTP_201_CREATED)

class RecursoDetailApiView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def get_object(self, fn, object_id):
            try:
                return fn.objects.get(id=object_id)
            except fn.DoesNotExist:
                return None
            
    def get(self, request, recurso_id, *args, **kwargs):

        recurso = self.get_object(Recursos, recurso_id)
        if not recurso:
            return Response(
                {"res": "Não existe recurso com o id informado"},
                status=st.HTTP_400_BAD_REQUEST
            )

        serializer = RecursoSerializer(recurso)
        return Response(serializer.data, status=st.HTTP_200_OK)

    def put(self, request, recurso_id, *args, **kwargs):
        recurso = self.get_object(Recursos, recurso_id)
        if not recurso:
                return Response(
                    {"res": "Não existe recurso com o id informado"}, 
                    status=st.HTTP_400_BAD_REQUEST
                )
        
        if request.data.get("proposta_projeto_id"):
            proposta_projeto = self.get_object(PropostaProjeto, request.data.get("proposta_projeto_id"))
            if not proposta_projeto:
                return Response(
                    {"res": "Não existe proposta de projeto com o id informado"}, 
                    status=st.HTTP_400_BAD_REQUEST
                )
            recurso.proposta_projeto = proposta_projeto

        if request.data.get("nome"):
            recurso.nome = request.data.get("nome")
        if request.data.get("descricao"):
            recurso.descricao = request.data.get("descricao")
        if request.data.get("quantidade"):
            recurso.quantidade = request.data.get("quantidade")
        if request.data.get("unidade"):
            recurso.unidade = request.data.get("unidade")
        if request.data.get("valor"):
            recurso.valor = request.data.get("valor")
        if request.data.get("valor_total"):
            recurso.valor_total = request.data.get("valor_total")
        if request.data.get("em_estoque") != None:
            recurso.em_estoque = request.data.get("em_estoque")
        recurso.save()
        serializer = RecursoSerializer(recurso)
        
        return Response(serializer.data, status=st.HTTP_200_OK)

    def delete(self, request, recurso_id, *args, **kwargs):
        
        recurso = self.get_object(Recursos, recurso_id)
        if not recurso:
            return Response(
                {"res": "Não existe recurso com o id informado"}, 
                status=st.HTTP_400_BAD_REQUEST
            )
        recurso.delete()
        return Response(
            {"res": "recurso deletado!"},
            status=st.HTTP_200_OK
        )
