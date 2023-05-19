# todo/todo_api/views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db import transaction
import json
from ..models.atividadeSection import AtividadeSection
from ..models.dpEvento import DpEvento
from ..models.atividade import Atividade
from ..models.servico import Servico
from ..serializers.atividadeSectionSerializer import AtividadeSectionSerializer
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

class AtividadeSectionApiView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def get(self, request, *args, **kwargs):
        evento_id = request.GET.get('evento_id') if request.GET.get('evento_id') != "None" else None
        atividadeSections = AtividadeSection.objects.prefetch_related('atividade_set')
        if evento_id:
            atividadeSections = atividadeSections.filter(evento__id=evento_id)

        atividadeSections = atividadeSections.order_by("order").all()
        
        serializer = AtividadeSectionSerializer(atividadeSections, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        data = json.loads(request.body)
        eventoId = data.get('evento_id')
        if not eventoId:
            return Response({'message': 'Evento não informado'}, status=status.HTTP_400_BAD_REQUEST)

        atividadeSection = AtividadeSection()
        atividadeSection.nome = data.get('nome') if data.get('nome') else None
        atividadeSection.order = data.get('order') if data.get('order') else None
        atividadeSection.evento = DpEvento.objects.get(id=eventoId)
        atividadeSection.save()
        atividadeSectionSerializer = AtividadeSectionSerializer(atividadeSection)
        return Response(atividadeSectionSerializer.data, status=status.HTTP_201_CREATED)

class AtividadeSectionDetailApiView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    
    def get_object(self, fn, object_id):
        try:
            return fn.objects.get(id=object_id)
        except fn.DoesNotExist:
            return None
            
    def get(self, request, atividade_section_id, *args, **kwargs):
        atividadeSection = self.get_object(AtividadeSection, atividade_section_id)
        if not atividadeSection:
            return Response(
                {"res": "Não existe seção de atividades com o id informado"},
                status=status.HTTP_400_BAD_REQUEST
            )
        serializer = AtividadeSectionSerializer(atividadeSection)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, atividade_section_id, *args, **kwargs):
        atividadeSection = self.get_object(AtividadeSection, atividade_section_id)
        if not atividadeSection:
            return Response(
                {"res": "Não existe seção de atividade com o id informado"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        print("atividadeSection antes: ", atividadeSection.id, atividadeSection.order)
        if request.data.get("nome"):
            atividadeSection.nome = request.data.get("nome")
        if request.data.get("order"):
            print("order: ",request.data.get("order"))
            atividadeSection.order = request.data.get("order")
        
        atividadeSection.save()
        print("atividadeSection depois: ", atividadeSection.id, atividadeSection.order)
        serializer = AtividadeSectionSerializer(atividadeSection)
        return Response(serializer.data, status=status.HTTP_200_OK)
        
    def delete(self, request, atividade_section_id, *args, **kwargs):
        atividadeSection = self.get_object(AtividadeSection, atividade_section_id)
        if not atividadeSection:
            return Response(
                {"res": "Não existe seção de atividade com o id informado"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        with transaction.atomic():
            atividades = Atividade.objects.filter(atividadeSection__id=atividade_section_id)
            for atividade in atividades:
                servicos = Servico.objects.filter(atividade__id=atividade.id)
                for servico in servicos:
                    servico.delete()
                atividade.delete()

            atividadeSection.delete()

        return Response(
            {"res": "seção de atividades deletada!"},
            status=status.HTTP_200_OK
        )
