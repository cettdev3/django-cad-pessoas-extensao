# todo/todo_api/views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions
from django.utils import timezone
from ..serializers.avaliacaoSerializer import AvaliacaoSerializer
from ..models.avaliacao import Avaliacao
from ..models.acao import Acao
from ..models.cidade import Cidade
from ..models.dpEvento import DpEvento
from ..models.membroExecucao import MembroExecucao
from ..serializers.pessoaSerializer import PessoaSerializer
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from datetime import datetime
import ntplib


class AvaliacaoApiView(APIView):
    # permission_classes = [IsAuthenticated]
    # authentication_classes = [TokenAuthentication, JWTAuthentication]

    def get_object(self, fn, object_id):
        try:
            return fn.objects.get(id=object_id)
        except fn.DoesNotExist:
            return None

    # 1. List all
    def get(self, request, *args, **kwargs):
        user = request.user
        # avaliacoes = Avaliacao.objects.filter(avaliador__pessoa__user__id=user.id)
        avaliacoes = Avaliacao.objects.all()
        serializer = AvaliacaoSerializer(avaliacoes, many=True)
        print(serializer.data)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        print(request.data)
        acao = None
        evento = None
        avaliador = None
        cidade = None
        requestHasAcao = request.data.get("acao_id") is not None
        requestHasEvento = request.data.get("evento_id") is not None

        if (requestHasAcao and requestHasEvento) or (
            not requestHasAcao and not requestHasEvento
        ):
            return Response(
                {"res": "Informe o id da ação ou do evento"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if request.data.get("acao_id"):
            acao = self.get_object(Acao, request.data.get("acao_id"))
            if not acao:
                return Response(
                    {"res": "Não existe ação com o id informado"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

        if request.data.get("evento_id"):
            evento = self.get_object(DpEvento, request.data.get("evento_id"))
            if not evento:
                return Response(
                    {"res": "Não existe evento com o id informado"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

        if request.data.get("membro_execucao_id"):
            avaliador = self.get_object(
                MembroExecucao, request.data.get("membro_execucao_id")
            )
            if not avaliador:
                return Response(
                    {"res": "Não existe pessoa com o id informado"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

        if request.data.get("cidade_id"):
            cidade = self.get_object(Cidade, request.data.get("cidade_id"))
            if not cidade:
                return Response(
                    {"res": "Não existe cidade com o id informado"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

        data = {
            "bairro": request.data.get("bairro"),
            "logradouro": request.data.get("logradouro"),
            "cep": request.data.get("cep"),
            "complemento": request.data.get("complemento"),
            "acao": acao,
            "evento": evento,
            "avaliador": avaliador,
        }
        avaliacao = Avaliacao.objects.create(**data)
        serializer = AvaliacaoSerializer(avaliacao)

        return Response(serializer.data, status=status.HTTP_201_CREATED)


class AvaliacaoDetailApiView(APIView):
    def get_object(self, fn, object_id):
        try:
            return fn.objects.get(id=object_id)
        except fn.DoesNotExist:
            return None

    # 3. Retrieve
    def get(self, request, avaliacao_id, *args, **kwargs):
        avaliacao = self.get_object(avaliacao_id)
        if not avaliacao:
            return Response(
                {"res": "Não existe avaliação com o id informado"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        serializer = AvaliacaoSerializer(avaliacao)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # 4. Update
    def put(self, request, avaliacao_id, *args, **kwargs):
        print("dentro do put", avaliacao_id, request.data)
        tmz = timezone.get_current_timezone()
        ntp_client = ntplib.NTPClient()
        response = ntp_client.request("pool.ntp.org")
        current_time = datetime.fromtimestamp(response.tx_time, tz=tmz)

        avaliacao = self.get_object(Avaliacao, avaliacao_id)
        if not avaliacao:
            return Response(
                {"res": "Não existe avaliação com o id informado"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        data = {}

        if request.data.get("evento_id"):
            evento = self.get_object(DpEvento, request.data.get("evento_id"))
            if not evento:
                return Response(
                    {"res": "Não existe evento com o id informado"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            avaliacao.evento = evento

        if request.data.get("acao_id"):
            acao = self.get_object(Acao, request.data.get("acao_id"))
            if not acao:
                return Response(
                    {"res": "Não existe ação com o id informado"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            avaliacao.acao = acao

        if request.data.get("membro_execucao_id"):
            avaliador = self.get_object(
                MembroExecucao, request.data.get("membro_execucao_id")
            )
            if not avaliador:
                return Response(
                    {"res": "Não existe avaliador com o id informado"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            avaliacao.avaliador = avaliador

        if request.data.get("qtdSalas"):
            intQtdSalas = int(request.data.get("qtdSalas"))
            isEquals = avaliacao.qtdSalas == intQtdSalas
            if not isEquals:
                avaliacao.qtdSalas = intQtdSalas
                if request.data.get("qtdSalasUpdatedAt"):
                    avaliacao.qtdSalasUpdatedAt = datetime.strptime(
                        request.data.get("qtdSalasUpdatedAt"), "%Y-%m-%d %H:%M:%S.%f"
                    )
                else:
                    avaliacao.qtdSalasUpdatedAt = current_time

        if request.data.get("observacaoGeral"):
            isEquals = avaliacao.observacaoGeral == request.data.get("observacaoGeral")
            if not isEquals:
                avaliacao.observacaoGeral = request.data.get("observacaoGeral")
                if request.data.get("observacaoGeralUpdatedAt"):
                    avaliacao.observacaoGeralUpdatedAt = datetime.strptime(
                        request.data.get("observacaoGeralUpdatedAt"),
                        "%Y-%m-%d %H:%M:%S.%f",
                    )
                else:
                    avaliacao.observacaoGeralUpdatedAt = current_time

        avaliacao.save()
        serializer = AvaliacaoSerializer(avaliacao)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # 5. Delete
    def delete(self, request, avaliacao_id, *args, **kwargs):
        avaliacao = self.get_object(avaliacao_id)
        if not avaliacao:
            return Response(
                {"res": "Não existe avaliação com o id informado"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        avaliacao.delete()
        return Response({"res": "Avaliação deletada!"}, status=status.HTTP_200_OK)
