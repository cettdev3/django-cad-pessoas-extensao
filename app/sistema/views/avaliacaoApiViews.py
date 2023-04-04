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
        avaliacoes = Avaliacao.objects.select_related('avaliador__pessoa__user', 'evento', 'acao').exclude(evento=None)
        serializer = AvaliacaoSerializer(avaliacoes, many=True)
        print(serializer.data)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
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
        print(serializer.data)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # 4. Update
    def put(self, request, avaliacao_id, *args, **kwargs):
        print("dentro do put", avaliacao_id, request.data)
        tmz = timezone.get_current_timezone()
        ntp_client = ntplib.NTPClient()
        # response = ntp_client.request("pool.ntp.br")
        current_time = datetime.now(tz=tmz)
        print(current_time)

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

        if request.data.get("geralTamanhoEspaco"):
            isEquals = avaliacao.geralTamanhoEspaco == request.data.get(
                "geralTamanhoEspaco"
            )
            if not isEquals:
                avaliacao.geralTamanhoEspaco = request.data.get("geralTamanhoEspaco")
                if request.data.get("geralTamanhoEspacoUpdatedAt"):
                    avaliacao.geralTamanhoEspacoUpdatedAt = datetime.strptime(
                        request.data.get("geralTamanhoEspacoUpdatedAt"),
                        "%Y-%m-%d %H:%M:%S.%f",
                    )
                else:
                    avaliacao.geralTamanhoEspacoUpdatedAt = current_time

        if request.data.get("geralQuantidadeDataShow"):
            isEquals = avaliacao.geralQuantidadeDataShow == request.data.get(
                "geralQuantidadeDataShow"
            )
            if not isEquals:
                avaliacao.geralQuantidadeDataShow = request.data.get(
                    "geralQuantidadeDataShow"
                )
                if request.data.get("geralQuantidadeDataShowUpdatedAt"):
                    avaliacao.geralQuantidadeDataShowUpdatedAt = datetime.strptime(
                        request.data.get("geralQuantidadeDataShowUpdatedAt"),
                        "%Y-%m-%d %H:%M:%S.%f",
                    )
                else:
                    avaliacao.geralQuantidadeDataShowUpdatedAt = current_time

        if request.data.get("geralHasBebedouro"):
            isEquals = avaliacao.geralHasBebedouro == request.data.get(
                "geralHasBebedouro"
            )
            if not isEquals:
                avaliacao.geralHasBebedouro = request.data.get(
                    "geralHasBebedouro"
                )
                if request.data.get("geralHasBebedouroUpdatedAt"):
                    avaliacao.geralHasBebedouroUpdatedAt = datetime.strptime(
                        request.data.get("geralHasBebedouroUpdatedAt"),
                        "%Y-%m-%d %H:%M:%S.%f",
                    )
                else:
                    avaliacao.geralHasBebedouroUpdatedAt = current_time
        
        if request.data.get("geralHasRedeEletrica"):
            isEquals = avaliacao.geralHasRedeEletrica == request.data.get(
                "geralHasRedeEletrica"
            )
            if not isEquals:
                avaliacao.geralHasRedeEletrica = request.data.get(
                    "geralHasRedeEletrica"
                )
                if request.data.get("geralHasRedeEletricaUpdatedAt"):
                    avaliacao.geralHasRedeEletricaUpdatedAt = datetime.strptime(
                        request.data.get("geralHasRedeEletricaUpdatedAt"),
                        "%Y-%m-%d %H:%M:%S.%f",
                    )
                else:
                    avaliacao.geralHasRedeEletricaUpdatedAt = current_time
        # geralHasCadeiras
        # geralHasCadeirasUpdatedAt
        if request.data.get("geralHasCadeiras"):
            isEquals = avaliacao.geralHasCadeiras == request.data.get(
                "geralHasCadeiras"
            )
            if not isEquals:
                avaliacao.geralHasCadeiras = request.data.get(
                    "geralHasCadeiras"
                )
                if request.data.get("geralHasCadeirasUpdatedAt"):
                    avaliacao.geralHasCadeirasUpdatedAt = datetime.strptime(
                        request.data.get("geralHasCadeirasUpdatedAt"),
                        "%Y-%m-%d %H:%M:%S.%f",
                    )
                else:
                    avaliacao.geralHasCadeirasUpdatedAt = current_time
        # geralHasEquipeLimpeza
        # geralHasEquipeLimpezaUpdatedAt
        if request.data.get("geralHasEquipeLimpeza"):
            isEquals = avaliacao.geralHasEquipeLimpeza == request.data.get(
                "geralHasEquipeLimpeza"
            )
            if not isEquals:
                avaliacao.geralHasEquipeLimpeza = request.data.get(
                    "geralHasEquipeLimpeza"
                )
                if request.data.get("geralHasEquipeLimpezaUpdatedAt"):
                    avaliacao.geralHasEquipeLimpezaUpdatedAt = datetime.strptime(
                        request.data.get("geralHasEquipeLimpezaUpdatedAt"),
                        "%Y-%m-%d %H:%M:%S.%f",
                    )
                else:
                    avaliacao.geralHasEquipeLimpezaUpdatedAt = current_time
        # geralHasIluminacao
        # geralHasIluminacaoUpdatedAt
        if request.data.get("geralHasIluminacao"):
            isEquals = avaliacao.geralHasIluminacao == request.data.get(
                "geralHasIluminacao"
            )
            if not isEquals:
                avaliacao.geralHasIluminacao = request.data.get(
                    "geralHasIluminacao"
                )
                if request.data.get("geralHasIluminacaoUpdatedAt"):
                    avaliacao.geralHasIluminacaoUpdatedAt = datetime.strptime(
                        request.data.get("geralHasIluminacaoUpdatedAt"),
                        "%Y-%m-%d %H:%M:%S.%f",
                    )
                else:
                    avaliacao.geralHasIluminacaoUpdatedAt = current_time
        # geralQuantidadeJanelas
        # geralQuantidadeJanelasUpdatedAt
        if request.data.get("geralQuantidadeJanelas"):
            isEquals = avaliacao.geralQuantidadeJanelas == request.data.get(
                "geralQuantidadeJanelas"
            )
            if not isEquals:
                avaliacao.geralQuantidadeJanelas = request.data.get(
                    "geralQuantidadeJanelas"
                )
                if request.data.get("geralQuantidadeJanelasUpdatedAt"):
                    avaliacao.geralQuantidadeJanelasUpdatedAt = datetime.strptime(
                        request.data.get("geralQuantidadeJanelasUpdatedAt"),
                        "%Y-%m-%d %H:%M:%S.%f",
                    )
                else:
                    avaliacao.geralQuantidadeJanelasUpdatedAt = current_time
        # geralQuantidadeBanheiros
        # geralQuantidadeBanheirosUpdatedAt
        if request.data.get("geralQuantidadeBanheiros"):
            isEquals = avaliacao.geralQuantidadeBanheiros == request.data.get(
                "geralQuantidadeBanheiros"
            )
            if not isEquals:
                avaliacao.geralQuantidadeBanheiros = request.data.get(
                    "geralQuantidadeBanheiros"
                )
                if request.data.get("geralQuantidadeBanheirosUpdatedAt"):
                    avaliacao.geralQuantidadeBanheirosUpdatedAt = datetime.strptime(
                        request.data.get("geralQuantidadeBanheirosUpdatedAt"),
                        "%Y-%m-%d %H:%M:%S.%f",
                    )
                else:
                    avaliacao.geralQuantidadeBanheirosUpdatedAt = current_time
        # salaCulinariaHasEspacoTurmas40Alunos
        # salaCulinariaHasEspacoTurmas40AlunosUpdatedAt
        if request.data.get("salaCulinariaHasEspacoTurmas40Alunos"):
            isEquals = avaliacao.salaCulinariaHasEspacoTurmas40Alunos == request.data.get(
                "salaCulinariaHasEspacoTurmas40Alunos"
            )
            if not isEquals:
                avaliacao.salaCulinariaHasEspacoTurmas40Alunos = request.data.get(
                    "salaCulinariaHasEspacoTurmas40Alunos"
                )
                if request.data.get("salaCulinariaHasEspacoTurmas40AlunosUpdatedAt"):
                    avaliacao.salaCulinariaHasEspacoTurmas40AlunosUpdatedAt = datetime.strptime(
                        request.data.get("salaCulinariaHasEspacoTurmas40AlunosUpdatedAt"),
                        "%Y-%m-%d %H:%M:%S.%f",
                    )
                else:
                    avaliacao.salaCulinariaHasEspacoTurmas40AlunosUpdatedAt = current_time
        # salaCulinariaHasVentilacao
        # salaCulinariaHasVentilacaoUpdatedAt
        if request.data.get("salaCulinariaHasVentilacao"):
            isEquals = avaliacao.salaCulinariaHasVentilacao == request.data.get(
                "salaCulinariaHasVentilacao"
            )
            if not isEquals:
                avaliacao.salaCulinariaHasVentilacao = request.data.get(
                    "salaCulinariaHasVentilacao"
                )
                if request.data.get("salaCulinariaHasVentilacaoUpdatedAt"):
                    avaliacao.salaCulinariaHasVentilacaoUpdatedAt = datetime.strptime(
                        request.data.get("salaCulinariaHasVentilacaoUpdatedAt"),
                        "%Y-%m-%d %H:%M:%S.%f",
                    )
                else:
                    avaliacao.salaCulinariaHasVentilacaoUpdatedAt = current_time
        # salaCulinariaQuantidadeTomadas
        # salaCulinariaQuantidadeTomadasUpdatedAt
        if request.data.get("salaCulinariaQuantidadeTomadas"):
            isEquals = avaliacao.salaCulinariaQuantidadeTomadas == request.data.get(
                "salaCulinariaQuantidadeTomadas"
            )
            if not isEquals:
                avaliacao.salaCulinariaQuantidadeTomadas = request.data.get(
                    "salaCulinariaQuantidadeTomadas"
                )
                if request.data.get("salaCulinariaQuantidadeTomadasUpdatedAt"):
                    avaliacao.salaCulinariaQuantidadeTomadasUpdatedAt = datetime.strptime(
                        request.data.get("salaCulinariaQuantidadeTomadasUpdatedAt"),
                        "%Y-%m-%d %H:%M:%S.%f",
                    )
                else:
                    avaliacao.salaCulinariaQuantidadeTomadasUpdatedAt = current_time
        # salaCulinariaQuantidadeFogoesFuncionando
        # salaCulinariaQuantidadeFogoesFuncionandoUpdatedAt
        if request.data.get("salaCulinariaQuantidadeFogoesFuncionando"):
            isEquals = avaliacao.salaCulinariaQuantidadeFogoesFuncionando == request.data.get(
                "salaCulinariaQuantidadeFogoesFuncionando"
            )
            if not isEquals:
                avaliacao.salaCulinariaQuantidadeFogoesFuncionando = request.data.get(
                    "salaCulinariaQuantidadeFogoesFuncionando"
                )
                if request.data.get("salaCulinariaQuantidadeFogoesFuncionandoUpdatedAt"):
                    avaliacao.salaCulinariaQuantidadeFogoesFuncionandoUpdatedAt = datetime.strptime(
                        request.data.get("salaCulinariaQuantidadeFogoesFuncionandoUpdatedAt"),
                        "%Y-%m-%d %H:%M:%S.%f",
                    )
                else:
                    avaliacao.salaCulinariaQuantidadeFogoesFuncionandoUpdatedAt = current_time
        # salaCulinariaQuantidadeFornosFuncionando
        # salaCulinariaQuantidadeFornosFuncionandoUpdatedAt
        if request.data.get("salaCulinariaQuantidadeFornosFuncionando"):
            isEquals = avaliacao.salaCulinariaQuantidadeFornosFuncionando == request.data.get(
                "salaCulinariaQuantidadeFornosFuncionando"
            )
            if not isEquals:
                avaliacao.salaCulinariaQuantidadeFornosFuncionando = request.data.get(
                    "salaCulinariaQuantidadeFornosFuncionando"
                )
                if request.data.get("salaCulinariaQuantidadeFornosFuncionandoUpdatedAt"):
                    avaliacao.salaCulinariaQuantidadeFornosFuncionandoUpdatedAt = datetime.strptime(
                        request.data.get("salaCulinariaQuantidadeFornosFuncionandoUpdatedAt"),
                        "%Y-%m-%d %H:%M:%S.%f",
                    )
                else:
                    avaliacao.salaCulinariaQuantidadeFornosFuncionandoUpdatedAt = current_time
        # salaCulinariaHasIluminacaoAdequada
        # salaCulinariaHasIluminacaoAdequadaUpdatedAt
        if request.data.get("salaCulinariaHasIluminacaoAdequada"):
            isEquals = avaliacao.salaCulinariaHasIluminacaoAdequada == request.data.get(
                "salaCulinariaHasIluminacaoAdequada"
            )
            if not isEquals:
                avaliacao.salaCulinariaHasIluminacaoAdequada = request.data.get(
                    "salaCulinariaHasIluminacaoAdequada"
                )
                if request.data.get("salaCulinariaHasIluminacaoAdequadaUpdatedAt"):
                    avaliacao.salaCulinariaHasIluminacaoAdequadaUpdatedAt = datetime.strptime(
                        request.data.get("salaCulinariaHasIluminacaoAdequadaUpdatedAt"),
                        "%Y-%m-%d %H:%M:%S.%f",
                    )
                else:
                    avaliacao.salaCulinariaHasIluminacaoAdequadaUpdatedAt = current_time
        # salaCulinariaQuantidadeGeladeirasFuncionando
        # salaCulinariaQuantidadeGeladeirasFuncionandoUpdatedAt
        if request.data.get("salaCulinariaQuantidadeGeladeirasFuncionando"):
            isEquals = avaliacao.salaCulinariaQuantidadeGeladeirasFuncionando == request.data.get(
                "salaCulinariaQuantidadeGeladeirasFuncionando"
            )
            if not isEquals:
                avaliacao.salaCulinariaQuantidadeGeladeirasFuncionando = request.data.get(
                    "salaCulinariaQuantidadeGeladeirasFuncionando"
                )
                if request.data.get("salaCulinariaQuantidadeGeladeirasFuncionandoUpdatedAt"):
                    avaliacao.salaCulinariaQuantidadeGeladeirasFuncionandoUpdatedAt = datetime.strptime(
                        request.data.get("salaCulinariaQuantidadeGeladeirasFuncionandoUpdatedAt"),
                        "%Y-%m-%d %H:%M:%S.%f",
                    )
                else:
                    avaliacao.salaCulinariaQuantidadeGeladeirasFuncionandoUpdatedAt = current_time
        # salaCulinariaQuantidadeMesasBancadas
        # salaCulinariaQuantidadeMesasBancadasUpdatedAt
        if request.data.get("salaCulinariaQuantidadeMesasBancadas"):
            isEquals = avaliacao.salaCulinariaQuantidadeMesasBancadas == request.data.get(
                "salaCulinariaQuantidadeMesasBancadas"
            )
            if not isEquals:
                avaliacao.salaCulinariaQuantidadeMesasBancadas = request.data.get(
                    "salaCulinariaQuantidadeMesasBancadas"
                )
                if request.data.get("salaCulinariaQuantidadeMesasBancadasUpdatedAt"):
                    avaliacao.salaCulinariaQuantidadeMesasBancadasUpdatedAt = datetime.strptime(
                        request.data.get("salaCulinariaQuantidadeMesasBancadasUpdatedAt"),
                        "%Y-%m-%d %H:%M:%S.%f",
                    )
                else:
                    avaliacao.salaCulinariaQuantidadeMesasBancadasUpdatedAt = current_time  
        # salaCulinariaQuantidadePiasComTorneiraFuncionando
        # salaCulinariaQuantidadePiasComTorneiraFuncionandoUpdatedAt
        if request.data.get("salaCulinariaQuantidadePiasComTorneiraFuncionando"):
            isEquals = avaliacao.salaCulinariaQuantidadePiasComTorneiraFuncionando == request.data.get(
                "salaCulinariaQuantidadePiasComTorneiraFuncionando"
            )
            if not isEquals:
                avaliacao.salaCulinariaQuantidadePiasComTorneiraFuncionando = request.data.get(
                    "salaCulinariaQuantidadePiasComTorneiraFuncionando"
                )
                if request.data.get("salaCulinariaQuantidadePiasComTorneiraFuncionandoUpdatedAt"):
                    avaliacao.salaCulinariaQuantidadePiasComTorneiraFuncionandoUpdatedAt = datetime.strptime(
                        request.data.get("salaCulinariaQuantidadePiasComTorneiraFuncionandoUpdatedAt"),
                        "%Y-%m-%d %H:%M:%S.%f",
                    )
                else:
                    avaliacao.salaCulinariaQuantidadePiasComTorneiraFuncionandoUpdatedAt = current_time
        # salaCulinariaQuantidadeVasilhamesGasComGas
        # salaCulinariaQuantidadeVasilhamesGasComGasUpdatedAt
        if request.data.get("salaCulinariaQuantidadeVasilhamesGasComGas"):
            isEquals = avaliacao.salaCulinariaQuantidadeVasilhamesGasComGas == request.data.get(
                "salaCulinariaQuantidadeVasilhamesGasComGas"
            )
            if not isEquals:
                avaliacao.salaCulinariaQuantidadeVasilhamesGasComGas = request.data.get(
                    "salaCulinariaQuantidadeVasilhamesGasComGas"
                )
                if request.data.get("salaCulinariaQuantidadeVasilhamesGasComGasUpdatedAt"):
                    avaliacao.salaCulinariaQuantidadeVasilhamesGasComGasUpdatedAt = datetime.strptime(
                        request.data.get("salaCulinariaQuantidadeVasilhamesGasComGasUpdatedAt"),
                        "%Y-%m-%d %H:%M:%S.%f",
                    )
                else:
                    avaliacao.salaCulinariaQuantidadeVasilhamesGasComGasUpdatedAt = current_time
        # salaCulinariaQuantidadeVasilhamesGasVazios
        # salaCulinariaQuantidadeVasilhamesGasVaziosUpdatedAt
        if request.data.get("salaCulinariaQuantidadeVasilhamesGasVazios"):
            isEquals = avaliacao.salaCulinariaQuantidadeVasilhamesGasVazios == request.data.get(
                "salaCulinariaQuantidadeVasilhamesGasVazios"
            )
            if not isEquals:
                avaliacao.salaCulinariaQuantidadeVasilhamesGasVazios = request.data.get(
                    "salaCulinariaQuantidadeVasilhamesGasVazios"
                )
                if request.data.get("salaCulinariaQuantidadeVasilhamesGasVaziosUpdatedAt"):
                    avaliacao.salaCulinariaQuantidadeVasilhamesGasVaziosUpdatedAt = datetime.strptime(
                        request.data.get("salaCulinariaQuantidadeVasilhamesGasVaziosUpdatedAt"),
                        "%Y-%m-%d %H:%M:%S.%f",
                    )
                else:
                    avaliacao.salaCulinariaQuantidadeVasilhamesGasVaziosUpdatedAt = current_time
        # salaCulinariaObservacao
        # salaCulinariaObservacaoUpdatedAt
        if request.data.get("salaCulinariaObservacao"):
            isEquals = avaliacao.salaCulinariaObservacao == request.data.get(
                "salaCulinariaObservacao"
            )
            if not isEquals:
                avaliacao.salaCulinariaObservacao = request.data.get(
                    "salaCulinariaObservacao"
                )
                if request.data.get("salaCulinariaObservacaoUpdatedAt"):
                    avaliacao.salaCulinariaObservacaoUpdatedAt = datetime.strptime(
                        request.data.get("salaCulinariaObservacaoUpdatedAt"),
                        "%Y-%m-%d %H:%M:%S.%f",
                    )
                else:
                    avaliacao.salaCulinariaObservacaoUpdatedAt = current_time
        # salaServicosBelezaHasPontoAguaExterno
        # salaServicosBelezaHasPontoAguaExternoUpdatedAt
        if request.data.get("salaServicosBelezaHasPontoAguaExterno"):
            isEquals = avaliacao.salaServicosBelezaHasPontoAguaExterno == request.data.get(
                "salaServicosBelezaHasPontoAguaExterno"
            )
            if not isEquals:
                avaliacao.salaServicosBelezaHasPontoAguaExterno = request.data.get(
                    "salaServicosBelezaHasPontoAguaExterno"
                )
                if request.data.get("salaServicosBelezaHasPontoAguaExternoUpdatedAt"):
                    avaliacao.salaServicosBelezaHasPontoAguaExternoUpdatedAt = datetime.strptime(
                        request.data.get("salaServicosBelezaHasPontoAguaExternoUpdatedAt"),
                        "%Y-%m-%d %H:%M:%S.%f",
                    )
                else:
                    avaliacao.salaServicosBelezaHasPontoAguaExternoUpdatedAt = current_time
        # salaServicosBelezaQuantidadePiasHigienizacao
        # salaServicosBelezaQuantidadePiasHigienizacaoUpdatedAt
        if request.data.get("salaServicosBelezaQuantidadePiasHigienizacao"):
            isEquals = avaliacao.salaServicosBelezaQuantidadePiasHigienizacao == request.data.get(
                "salaServicosBelezaQuantidadePiasHigienizacao"
            )
            if not isEquals:
                avaliacao.salaServicosBelezaQuantidadePiasHigienizacao = request.data.get(
                    "salaServicosBelezaQuantidadePiasHigienizacao"
                )
                if request.data.get("salaServicosBelezaQuantidadePiasHigienizacaoUpdatedAt"):
                    avaliacao.salaServicosBelezaQuantidadePiasHigienizacaoUpdatedAt = datetime.strptime(
                        request.data.get("salaServicosBelezaQuantidadePiasHigienizacaoUpdatedAt"),
                        "%Y-%m-%d %H:%M:%S.%f",
                    )
                else:
                    avaliacao.salaServicosBelezaQuantidadePiasHigienizacaoUpdatedAt = current_time
        # salaServicosBelezaQuantidadeCadeirasSalao
        # salaServicosBelezaQuantidadeCadeirasSalaoUpdatedAt
        if request.data.get("salaServicosBelezaQuantidadeCadeirasSalao"):
            isEquals = avaliacao.salaServicosBelezaQuantidadeCadeirasSalao == request.data.get(
                "salaServicosBelezaQuantidadeCadeirasSalao"
            )
            if not isEquals:
                avaliacao.salaServicosBelezaQuantidadeCadeirasSalao = request.data.get(
                    "salaServicosBelezaQuantidadeCadeirasSalao"
                )
                if request.data.get("salaServicosBelezaQuantidadeCadeirasSalaoUpdatedAt"):
                    avaliacao.salaServicosBelezaQuantidadeCadeirasSalaoUpdatedAt = datetime.strptime(
                        request.data.get("salaServicosBelezaQuantidadeCadeirasSalaoUpdatedAt"),
                        "%Y-%m-%d %H:%M:%S.%f",
                    )
                else:
                    avaliacao.salaServicosBelezaQuantidadeCadeirasSalaoUpdatedAt = current_time
        # salaServicosBelezaObservacao
        # salaServicosBelezaObservacaoUpdatedAt
        if request.data.get("salaServicosBelezaObservacao"):
            isEquals = avaliacao.salaServicosBelezaObservacao == request.data.get(
                "salaServicosBelezaObservacao"
            )
            if not isEquals:
                avaliacao.salaServicosBelezaObservacao = request.data.get(
                    "salaServicosBelezaObservacao"
                )
                if request.data.get("salaServicosBelezaObservacaoUpdatedAt"):
                    avaliacao.salaServicosBelezaObservacaoUpdatedAt = datetime.strptime(
                        request.data.get("salaServicosBelezaObservacaoUpdatedAt"),
                        "%Y-%m-%d %H:%M:%S.%f",
                    )
                else:
                    avaliacao.salaServicosBelezaObservacaoUpdatedAt = current_time

        if request.data.get("cidade_id"):
            cidade = self.get_object(Cidade, request.data.get("cidade_id"))
            if not cidade:
                return Response(
                    {"res": "Não existe cidade com o id informado"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            avaliacao.cidade = cidade
        if request.data.get("bairro"):
            avaliacao.bairro = request.data.get("bairro")
        if request.data.get("logradouro"):
            avaliacao.logradouro = request.data.get("logradouro")
        if request.data.get("cep"):
            avaliacao.cep = request.data.get("cep")
        if request.data.get("complemento"):
            avaliacao.complemento = request.data.get("complemento")
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
