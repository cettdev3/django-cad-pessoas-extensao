# todo/todo_api/views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db import transaction

from django.db.models import Prefetch
from ..models.dpEvento import DpEvento
from ..models.ticket import Ticket
from ..models.cidade import Cidade
from ..models.escola import Escola
from ..models.itinerario import Itinerario
from ..models.atividade import Atividade
from ..models.ensino import Ensino
from ..models.imagem import Imagem
from ..models.avaliacao import Avaliacao
from ..models.itinerarioItem import ItinerarioItem
from ..models.membroExecucao import MembroExecucao
from ..serializers.dpEventoSerializer import DpEventoSerializer
from ..serializers.membroExecucaoSerializer import MembroExecucaoSerializer
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from django.db import reset_queries
from datetime import datetime
from django.db import connection
from django.db.models import Q
import requests
from ..services.alfrescoApi import AlfrescoAPI

def parse_date(date_string, formats):
    for fmt in formats:
        try:
            return datetime.strptime(date_string, fmt).date()
        except ValueError:
            pass
    return None
class DpEventoApiView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    
    def get_object(self, fn, object_id):
        try:
            return fn.objects.get(id=object_id)
        except fn.DoesNotExist:
            return None

    def get(self, request, *args, **kwargs):

        print("dentro do get de dpEvento")
        dp_eventos = DpEvento.objects.prefetch_related(Prefetch(
            'membroexecucao_set',
            queryset=MembroExecucao.objects.order_by('ticket__status').distinct()
        ))
        for dp_evento in dp_eventos:
            membros_execucao = dp_evento.membroexecucao_set.all()
        if request.GET.get("tipo"):
            dp_eventos = dp_eventos.filter(tipo__icontains=request.GET.get("tipo"))
        if request.GET.get('data_inicio') and not request.GET.get('data_fim'):
            dp_eventos = dp_eventos.filter(data_inicio__gte=request.GET.get('data_inicio'))
        if request.GET.get('data_fim') and not request.GET.get('data_inicio'):
            dp_eventos = dp_eventos.filter(data_fim__lte=request.GET.get('data_fim'))
        if request.GET.get('data_inicio') and request.GET.get('data_fim'):
            data_fim = datetime.strptime(request.GET.get('data_fim'), '%Y-%m-%d')
            data_fim = datetime.combine(data_fim, datetime.max.time())
            data_inicio = datetime.strptime(request.GET.get('data_inicio'), '%Y-%m-%d')
            data_inicio = datetime.combine(data_inicio, datetime.min.time())
            dp_eventos = dp_eventos.filter(Q(data_inicio__range=[data_inicio, data_fim]) | 
                                 Q(data_fim__range=[data_inicio, data_fim]))
        if request.GET.get("order_by"):
            dp_eventos = dp_eventos.order_by(request.GET.get("order_by"))
        else:
            dp_eventos = dp_eventos.order_by("-data_inicio")

        reset_queries()
        dp_eventos = dp_eventos.all()
        serializer = DpEventoSerializer(dp_eventos, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        cidade = None
        escola = None
        acaoEnsino = None
        postDpEventoData = request.data.get("dpEvento")
        postItinerariosData = request.data.get("itinerarios")

        if postDpEventoData["cidade_id"]:
            cidade = self.get_object(Cidade, postDpEventoData["cidade_id"])
            if not cidade:
                return Response(
                    {"res": "Não existe cidade com o id informado"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

        if postDpEventoData["escola_id"]:
            escola = self.get_object(Escola, postDpEventoData["escola_id"])
            if not escola:
                return Response(
                    {"res": "Não existe escola com o id informado"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
        
        if postDpEventoData["acao_ensino_id"]:
            acaoEnsino = self.get_object(Ensino, postDpEventoData["acao_ensino_id"])
            if not acaoEnsino:
                return Response(
                    {"res": "Não existe ação de ensino com o id informado"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
        
        date_formats = ['%Y-%m-%d', '%Y-%m-%dT%H:%M']
        dataInicio = None
        if postDpEventoData["data_inicio"]:
            dataInicio = parse_date(postDpEventoData["data_inicio"], date_formats)

        dataFim = None
        if postDpEventoData["data_fim"]:
            dataFim = parse_date(postDpEventoData["data_fim"], date_formats)

        dp_eventoData = {
            "tipo": postDpEventoData["tipo"] if postDpEventoData["tipo"] else None,
            "descricao": postDpEventoData["descricao"] if postDpEventoData["descricao"] else None,
            "data_inicio": dataInicio,
            "data_fim": dataFim,
            "bairro": postDpEventoData["bairro"] if postDpEventoData["bairro"] else None,
            "logradouro": postDpEventoData["logradouro"] if postDpEventoData["logradouro"] else None,
            "cep": postDpEventoData["cep"] if postDpEventoData["cep"] else None,
            "complemento": postDpEventoData["complemento"] if postDpEventoData["complemento"] else None,
            "cidade": cidade,
            "escola": escola,
            "acaoEnsino": acaoEnsino,
        }

        membrosExecucaoData = []
        
        dp_eventoData = DpEvento.objects.create(**dp_eventoData)
        dp_eventoSerializer = DpEventoSerializer(dp_eventoData)
        print("dados salvos", dp_eventoSerializer.data)
        return Response(dp_eventoSerializer.data, status=status.HTTP_200_OK)

class DpEventoDetailApiView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def get_object(self, fn, object_id):
        try:
            return fn.objects.get(id=object_id)
        except fn.DoesNotExist:
            return None

    def get(self, request, dp_evento_id, *args, **kwargs):
        print("dentro do fet")
        dp_evento = DpEvento.objects.prefetch_related(
            Prefetch('membro_execucao_set', queryset=MembroExecucao.objects.prefetch_related('ticket_set'))
        ).get(id=dp_evento_id)
        if not dp_evento:
            return Response(
                {"res": "Não existe ação com o id informado"},
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = DpEventoSerializer(dp_evento)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, dp_evento_id, *args, **kwargs):
        dp_evento = self.get_object(DpEvento, dp_evento_id)
        if not dp_evento:
            return Response(
                {"res": "Não existe ação com o id informado"},
                status=status.HTTP_400_BAD_REQUEST
            )

        if request.data.get("tipo"):
            dp_evento.tipo = request.data.get("tipo")
        if request.data.get("descricao"):
            dp_evento.descricao = request.data.get("descricao")
        if request.data.get("data_inicio"):
            dp_evento.data_inicio = request.data.get("data_inicio")
        if request.data.get("data_fim"):
            dp_evento.data_fim = request.data.get("data_fim")
        if request.data.get("bairro"):
            dp_evento.bairro = request.data.get("bairro")
        if request.data.get("logradouro"):
            dp_evento.logradouro = request.data.get("logradouro")
        if request.data.get("cep"):
            dp_evento.cep = request.data.get("cep")
        if request.data.get("complemento"):
            dp_evento.complemento = request.data.get("complemento")
        if request.data.get("cidade_id"):
            cidade = self.get_object(Cidade, request.data.get("cidade_id"))
            if not cidade:
                return Response(
                    {"res": "Não existe cidade com o id informado"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            dp_evento.cidade = cidade

        if request.data.get("escola_id"):
            escola = self.get_object(Escola, request.data.get("escola_id"))
            if not escola:
                return Response(
                    {"res": "Não existe escola com o id informado"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            dp_evento.escola = escola
        
        print(request.data.get("acao_ensino_id"))
        if request.data.get("acao_ensino_id"):
            acaoEnsino = self.get_object(Ensino, request.data.get("acao_ensino_id"))
            if not acaoEnsino:
                return Response(
                    {"res": "Não existe ação de ensino com o id informado"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            dp_evento.acaoEnsino = acaoEnsino
        else:
            dp_evento.acaoEnsino = None

        dp_evento.save()
        serializer = DpEventoSerializer(dp_evento)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, dp_evento_id, *args, **kwargs):
        with transaction.atomic():
            instance = self.get_object(DpEvento, dp_evento_id)
            if not instance:
                return Response(
                    {"res": "Não existe ação com o id informado"},
                    status=status.HTTP_400_BAD_REQUEST
                )

            membrosExecucao = MembroExecucao.objects.filter(evento=instance)
            for membro_execucao in membrosExecucao:
                tickets = Ticket.objects.filter(membro_execucao=membro_execucao)
                for ticket in tickets:
                    ticket.delete()

                itinerario = Itinerario.objects.filter(membroexecucao=membro_execucao).first()
                if itinerario is not None:
                    itinerarioItems = ItinerarioItem.objects.filter(itinerario=itinerario)
                    for itinerarioItem in itinerarioItems:
                        itinerarioItem.delete()

                    itinerario.delete()

                membro_execucao.delete()
            for atividade in Atividade.objects.filter(evento=instance):
                galeria = atividade.galeria
                if galeria is not None:
                    alfrescoApi = AlfrescoAPI()
                    for imagem in Imagem.objects.filter(galeria=galeria):
                        alfrescoApi.deleteNode(imagem.id_alfresco)
                        imagem.delete()

                atividade.delete()

            for avaliacao in Avaliacao.objects.filter(evento=instance):
                avaliacao.delete()

            instance.delete()
        return Response(
            {"res": "ação deletada!"},
            status=status.HTTP_200_OK
        )