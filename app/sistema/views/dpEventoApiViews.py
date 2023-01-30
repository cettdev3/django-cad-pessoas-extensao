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
from ..models.itinerarioItem import ItinerarioItem
from ..models.membroExecucao import MembroExecucao
from ..serializers.dpEventoSerializer import DpEventoSerializer
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from django.db import reset_queries
from datetime import datetime
from django.db import connection

class DpEventoApiView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def get_object(self, fn, object_id):
        try:
            return fn.objects.get(id=object_id)
        except fn.DoesNotExist:
            return None

    def get(self, request, *args, **kwargs):
        print("kdsfjksahfljkashflkash")
        dp_eventos = DpEvento.objects.prefetch_related(Prefetch(
            'membroexecucao_set',
            queryset=MembroExecucao.objects.order_by('ticket__status')
        ))

        if request.GET.get("tipo"):
            dp_eventos = dp_eventos.filter(tipo__icontains=request.GET.get("tipo"))
        reset_queries()
        dp_eventos = dp_eventos.all()
        serializer = DpEventoSerializer(dp_eventos, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        cidade = None
        escola = None
        postDpEventoData = request.data.get("dpEvento")
        print("postDpEventoData", request.data)
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

        dp_eventoData = {
            "tipo": postDpEventoData["tipo"] if postDpEventoData["tipo"] else None,
            "descricao": postDpEventoData["descricao"] if postDpEventoData["descricao"] else None,
            "data_inicio": postDpEventoData["data_inicio"] if postDpEventoData["data_inicio"] else None,
            "data_fim": postDpEventoData["data_fim"] if postDpEventoData["data_fim"] else None,
            "bairro": postDpEventoData["bairro"] if postDpEventoData["bairro"] else None,
            "logradouro": postDpEventoData["logradouro"] if postDpEventoData["logradouro"] else None,
            "cep": postDpEventoData["cep"] if postDpEventoData["cep"] else None,
            "complemento": postDpEventoData["complemento"] if postDpEventoData["complemento"] else None,
            "cidade": cidade,
            "escola": escola,
        }

        membrosExecucaoData = []
        if len(postDpEventoData["membros_execucao"]):
            for membroExecucao in postDpEventoData["membros_execucao"]:
                membroExecucaoData = {
                    "pessoa_id": membroExecucao.get("pessoa_id") if membroExecucao.get("pessoa_id") else None,
                    "tipo": membroExecucao.get("tipo") if membroExecucao.get("tipo") else None,
                    "data_inicio": membroExecucao.get("data_inicio") if membroExecucao.get("data_inicio") else None,
                    "data_fim": membroExecucao.get("data_fim") if membroExecucao.get("data_fim") else None,
                    "cidade_id": membroExecucao.get("cidade_id") if membroExecucao.get("cidade_id") else None,
                    "complemento": membroExecucao.get("complemento") if membroExecucao.get("complemento") else None,
                    "cep": membroExecucao.get("cep") if membroExecucao.get("cep") else None,
                    "bairro": membroExecucao.get("bairro") if membroExecucao.get("bairro") else None,
                    "logradouro": membroExecucao.get("logradouro") if membroExecucao.get("logradouro") else None,
                }
                membrosExecucaoData.append(membroExecucaoData)
        
        with transaction.atomic():
            dp_eventoData = DpEvento.objects.create(**dp_eventoData)
            databaseMembrsoExecucao = []
            for membrosExecucaoData in membrosExecucaoData:
                membrosExecucaoData["evento"] = dp_eventoData
                membroExecucao = MembroExecucao.objects.create(**membrosExecucaoData)
                databaseMembrsoExecucao.append(membroExecucao)

            for itinerarioData in postItinerariosData:
                itinerario = Itinerario.objects.create(
                    color=itinerarioData["color"] if itinerarioData["color"] else None,
                )
                print("criando itinerario", itinerario.id)


                for postItinerarioItemData in itinerarioData["itens"]:
                    cidade = None
                    if postItinerarioItemData.get("cidade_id"):
                        cidade = self.get_object(Cidade, postItinerarioItemData["cidade_id"])
                        if not cidade:
                            return Response(
                                {"res": "Não existe cidade com o id informado"},
                                status=status.HTTP_400_BAD_REQUEST,
                            )
                    print("dados vindos do post: ",postItinerarioItemData)
                    data = postItinerarioItemData["data"] if postItinerarioItemData.get("data") else None
                    if data:
                        # convert str '2023-01-16T10:09' to datetime
                        data = datetime.strptime(data, '%Y-%m-%dT%H:%M')
                    itinerarioItemData = {
                        "data_hora": data,
                        "endereco": postItinerarioItemData["endereco"] if postItinerarioItemData.get("endereco") else None,
                        "bairro": postItinerarioItemData["bairro"] if postItinerarioItemData.get("bairro") else None,
                        "logradouro": postItinerarioItemData["logradouro"] if postItinerarioItemData.get("logradouro") else None,
                        "cep": postItinerarioItemData["cep"] if postItinerarioItemData.get("cep") else None,
                        "complemento": postItinerarioItemData["complemento"] if postItinerarioItemData.get("complemento") else None,
                        "cidade": cidade,
                        "escola": postItinerarioItemData["escola"] if postItinerarioItemData.get("escola") else None,
                        "latitude": postItinerarioItemData["latitude"] if postItinerarioItemData.get("latitude") else None,
                        "longitude": postItinerarioItemData["longitude"] if postItinerarioItemData.get("longitude") else None,
                        "itinerario": itinerario,
                    }

                    itinerarioItem = ItinerarioItem.objects.create(**itinerarioItemData)
                for membroExecucao in databaseMembrsoExecucao:
                    for itinerarioMembroEquipe in itinerarioData["membros_equipe"]:
                        isSamePerson = int(membroExecucao.pessoa.id) == int(itinerarioMembroEquipe["pessoa_id"])
                        isSameType = membroExecucao.tipo == itinerarioMembroEquipe["tipo_solicitacao"]
                        if isSamePerson and isSameType:
                            membroExecucao.itinerario = itinerario
                            membroExecucao.save()

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

        dp_evento = self.get_object(DpEvento, dp_evento_id)
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

        dp_evento.save()
        serializer = DpEventoSerializer(dp_evento)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, dp_evento_id, *args, **kwargs):

        dp_evento = self.get_object(DpEvento, dp_evento_id)
        if not dp_evento:
            return Response(
                {"res": "Não existe ação com o id informado"},
                status=status.HTTP_400_BAD_REQUEST
            )

        membrosExecucao = MembroExecucao.objects.filter(dp_evento_id=dp_evento_id)
        for membroExecucao in membrosExecucao:
            tickets = Ticket.objects.filter(
                membro_execucao_id=membroExecucao.id)
            for ticket in tickets:
                ticket.delete()
            membroExecucao.delete()

        dp_evento.delete()
        return Response(
            {"res": "ação deletada!"},
            status=status.HTTP_200_OK
        )