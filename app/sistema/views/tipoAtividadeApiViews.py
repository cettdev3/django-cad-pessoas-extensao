from datetime import datetime
from rest_framework.views import APIView
from django.db.models import Q
from rest_framework.response import Response
from rest_framework import status as st
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from ..models.tipoAtividade import TipoAtividade
from ..models.acao import Acao
from ..models.membroExecucao import MembroExecucao
from ..serializers.tipoAtividadeSerializer import TipoAtividadeSerializer 
from sistema.services.camunda import CamundaAPI 
import json
import time

class TipoAtividadeApiView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    
    def get_object(self, fn, object_id):
        try:
            return fn.objects.get(id=object_id)
        except fn.DoesNotExist:
            return None

    def get(self, request, *args, **kwargs):
        tiposAtividades = TipoAtividade.objects.all()
        serializer = TipoAtividadeSerializer(tiposAtividades, many=True)
        return Response(serializer.data, status=st.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        tipoAtividade = {
            "nome": request.data.get("nome"),
            "descricao": request.data.get("descricao"),
            "categoria": request.data.get("categoria"),
        }
    
        serializer = TipoAtividadeSerializer(data=tipoAtividade)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=st.HTTP_201_CREATED)
        return Response(serializer.errors, status=st.HTTP_400_BAD_REQUEST)

class TipoAtividadeDetailApiView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def get_object(self, fn, object_id):
        try:
            return fn.objects.get(id=object_id)
        except fn.DoesNotExist:
            return None
            
    def get(self, request, tipo_atividade_id, *args, **kwargs):

        tipoAtividade = self.get_object(TipoAtividade, tipo_atividade_id)
        if not tipoAtividade:
            return Response(
                {"res": "Não existe tipo de atividade com o id informado"},
                status=st.HTTP_400_BAD_REQUEST
            )

        serializer = TipoAtividadeSerializer(tipoAtividade)
        return Response(serializer.data, status=st.HTTP_200_OK)

    def put(self, request, tipo_atividade_id, *args, **kwargs):
        tipoAtividade = self.get_object(TipoAtividade, tipo_atividade_id)
        if not tipoAtividade:
                return Response(
                    {"res": "Não existe tipo de atividade com o id informado"}, 
                    status=st.HTTP_400_BAD_REQUEST
                )

        if request.data.get("nome"):
            tipoAtividade.nome = request.data.get("nome")
        if request.data.get("descricao"):
            tipoAtividade.descricao = request.data.get("descricao")
        if request.data.get("categoria"):
            tipoAtividade.categoria = request.data.get("categoria")
        
        tipoAtividade.save()
        serializer = TipoAtividadeSerializer(tipoAtividade)
        
        return Response(serializer.data, status=st.HTTP_200_OK)

    def delete(self, request, tipo_atividade_id, *args, **kwargs):
        
        tipoAtividade = self.get_object(TipoAtividade, tipo_atividade_id)
        if not tipoAtividade:
            return Response(
                {"res": "Não existe tipo de atividade com o id informado"}, 
                status=st.HTTP_400_BAD_REQUEST
            )
    
        # tipoAtividade.delete()
        return Response(
            {"res": "tipo de atividade deletado!"},
            status=st.HTTP_200_OK
        )