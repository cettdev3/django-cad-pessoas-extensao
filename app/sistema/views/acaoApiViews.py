# todo/todo_api/views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions
from django.db import transaction

from django.db.models import Prefetch
from ..models.acao import Acao
from ..models.ticket import Ticket
from ..models.cidade import Cidade
from ..models.escola import Escola
from ..models.itinerario import Itinerario
from ..models.itinerarioItem import ItinerarioItem
from ..models.membroExecucao import MembroExecucao
from ..serializers.acaoSerializer import AcaoSerializer
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from django.db import reset_queries
from django.db import connection

class AcaoApiView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def get_object(self, fn, object_id):
        try:
            return fn.objects.get(id=object_id)
        except fn.DoesNotExist:
            return None

    def get(self, request, *args, **kwargs):
        print("kdsfjksahfljkashflkash")
        acoes = Acao.objects.prefetch_related(Prefetch(
            'membroexecucao_set',
            queryset=MembroExecucao.objects.order_by('ticket__status')
        ))

        if request.GET.get("tipo"):
            acoes = acoes.filter(tipo__icontains=request.GET.get("tipo"))
        reset_queries()
        acoes = acoes.all()
        serializer = AcaoSerializer(acoes, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        cidade = None
        escola = None
        postAcaoData = request.data.get("acao")
        postItinerariosData = request.data.get("itinerarios")

        if postAcaoData["cidade_id"]:
            cidade = self.get_object(Cidade, postAcaoData["cidade_id"])
            if not cidade:
                return Response(
                    {"res": "Não existe cidade com o id informado"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

        if postAcaoData["escola_id"]:
            escola = self.get_object(Escola, postAcaoData["escola_id"])
            if not escola:
                return Response(
                    {"res": "Não existe escola com o id informado"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

        acaoData = {
            "tipo": postAcaoData["tipo"] if postAcaoData["tipo"] else None,
            "descricao": postAcaoData["descricao"] if postAcaoData["descricao"] else None,
            "data_inicio": postAcaoData["data_inicio"] if postAcaoData["data_inicio"] else None,
            "data_fim": postAcaoData["data_fim"] if postAcaoData["data_fim"] else None,
            "bairro": postAcaoData["bairro"] if postAcaoData["bairro"] else None,
            "logradouro": postAcaoData["logradouro"] if postAcaoData["logradouro"] else None,
            "cep": postAcaoData["cep"] if postAcaoData["cep"] else None,
            "complemento": postAcaoData["complemento"] if postAcaoData["complemento"] else None,
            "cidade": cidade,
            "escola": escola,
        }

        membrosExecucaoData = []
        if len(postAcaoData["membros_execucao"]):
            for membroExecucao in postAcaoData["membros_execucao"]:
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
            acaoData = Acao.objects.create(**acaoData)
            databaseMembrsoExecucao = []
            for membrosExecucaoData in membrosExecucaoData:
                membrosExecucaoData["acao"] = acaoData
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
                    itinerarioItemData = {
                        "data_hora": postItinerarioItemData["data"] if postItinerarioItemData.get("data") else None,
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

            acaoSerializer = AcaoSerializer(acaoData)
            print("dados salvos", acaoSerializer.data)
        return Response(acaoSerializer.data, status=status.HTTP_200_OK)

class AcaoDetailApiView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def get_object(self, fn, object_id):
        try:
            return fn.objects.get(id=object_id)
        except fn.DoesNotExist:
            return None

    def get(self, request, acao_id, *args, **kwargs):

        acao = self.get_object(Acao, acao_id)
        if not acao:
            return Response(
                {"res": "Não existe ação com o id informado"},
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = AcaoSerializer(acao)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, acao_id, *args, **kwargs):
        acao = self.get_object(Acao, acao_id)
        if not acao:
            return Response(
                {"res": "Não existe ação com o id informado"},
                status=status.HTTP_400_BAD_REQUEST
            )

        if request.data.get("tipo"):
            acao.tipo = request.data.get("tipo")
        if request.data.get("descricao"):
            acao.descricao = request.data.get("descricao")
        if request.data.get("data_inicio"):
            acao.data_inicio = request.data.get("data_inicio")
        if request.data.get("data_fim"):
            acao.data_fim = request.data.get("data_fim")
        if request.data.get("bairro"):
            acao.bairro = request.data.get("bairro")
        if request.data.get("logradouro"):
            acao.logradouro = request.data.get("logradouro")
        if request.data.get("cep"):
            acao.cep = request.data.get("cep")
        if request.data.get("complemento"):
            acao.complemento = request.data.get("complemento")
        if request.data.get("cidade_id"):
            cidade = self.get_object(Cidade, request.data.get("cidade_id"))
            if not cidade:
                return Response(
                    {"res": "Não existe cidade com o id informado"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            acao.cidade = cidade

        if request.data.get("escola_id"):
            escola = self.get_object(Escola, request.data.get("escola_id"))
            if not escola:
                return Response(
                    {"res": "Não existe escola com o id informado"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            acao.escola = escola

        acao.save()
        serializer = AcaoSerializer(acao)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, acao_id, *args, **kwargs):

        acao = self.get_object(Acao, acao_id)
        if not acao:
            return Response(
                {"res": "Não existe ação com o id informado"},
                status=status.HTTP_400_BAD_REQUEST
            )

        membrosExecucao = MembroExecucao.objects.filter(acao_id=acao_id)
        for membroExecucao in membrosExecucao:
            tickets = Ticket.objects.filter(
                membro_execucao_id=membroExecucao.id)
            for ticket in tickets:
                ticket.delete()
            membroExecucao.delete()

        acao.delete()
        return Response(
            {"res": "ação deletada!"},
            status=status.HTTP_200_OK
        )