# todo/todo_api/serializers.py
from rest_framework import serializers
from ..models.avaliacao import Avaliacao
from ..serializers.membroExecucaoSerializer import MembroExecucaoSerializer
from ..serializers.dpEventoSerializer import DpEventoSerializer
class AvaliacaoSerializer(serializers.ModelSerializer):
    endereco_completo = serializers.CharField(read_only=True)
    avaliador = MembroExecucaoSerializer(read_only=True)
    evento = DpEventoSerializer(read_only=True)
    class Meta:
        model = Avaliacao
        fields = [
            "id",
            "acao",
            "evento",
            "avaliador",
            "bairro",
            "logradouro",
            "cep",
            "complemento",
            "endereco_completo",
            "qtdSalas",
            "qtdSalasUpdatedAt",
            "observacaoGeral",
            "observacaoGeralUpdatedAt",
            "geralTamanhoEspaco",
            "geralTamanhoEspacoUpdatedAt",
            "geralQuantidadeDataShow",
            "geralQuantidadeDataShowUpdatedAt",
            "geralHasBebedouro",
            "geralHasBebedouroUpdatedAt",
            "geralHasRedeEletrica",
            "geralHasRedeEletricaUpdatedAt",
            "geralHasCadeiras",
            "geralHasCadeirasUpdatedAt",
            "geralHasEquipeLimpeza",
            "geralHasEquipeLimpezaUpdatedAt",
            "geralHasIluminacao",
            "geralHasIluminacaoUpdatedAt",
            "geralQuantidadeJanelas",
            "geralQuantidadeJanelasUpdatedAt",
            "geralQuantidadeBanheiros",
            "geralQuantidadeBanheirosUpdatedAt",
            "salaCulinariaHasEspacoTurmas40Alunos",
            "salaCulinariaHasEspacoTurmas40AlunosUpdatedAt",
            "salaCulinariaHasVentilacao",
            "salaCulinariaHasVentilacaoUpdatedAt",
            "salaCulinariaQuantidadeTomadas",
            "salaCulinariaQuantidadeTomadasUpdatedAt",
            "salaCulinariaQuantidadeFogoesFuncionando",
            "salaCulinariaQuantidadeFogoesFuncionandoUpdatedAt",
            "salaCulinariaQuantidadeFornosFuncionando",
            "salaCulinariaQuantidadeFornosFuncionandoUpdatedAt",
            "salaCulinariaHasIluminacaoAdequada",
            "salaCulinariaHasIluminacaoAdequadaUpdatedAt",
            "salaCulinariaQuantidadeGeladeirasFuncionando",
            "salaCulinariaQuantidadeGeladeirasFuncionandoUpdatedAt",
            "salaCulinariaQuantidadeMesasBancadas",
            "salaCulinariaQuantidadeMesasBancadasUpdatedAt",
            "salaCulinariaQuantidadePiasComTorneiraFuncionando",
            "salaCulinariaQuantidadePiasComTorneiraFuncionandoUpdatedAt",
            "salaCulinariaQuantidadeVasilhamesGasComGas",
            "salaCulinariaQuantidadeVasilhamesGasComGasUpdatedAt",
            "salaCulinariaQuantidadeVasilhamesGasVazios",
            "salaCulinariaQuantidadeVasilhamesGasVaziosUpdatedAt",
            "salaCulinariaObservacao",
            "salaCulinariaObservacaoUpdatedAt",
            "salaServicosBelezaHasPontoAguaExterno",
            "salaServicosBelezaHasPontoAguaExternoUpdatedAt",
            "salaServicosBelezaQuantidadePiasHigienizacao",
            "salaServicosBelezaQuantidadePiasHigienizacaoUpdatedAt",
            "salaServicosBelezaQuantidadeCadeirasSalao",
            "salaServicosBelezaQuantidadeCadeirasSalaoUpdatedAt",
            "salaServicosBelezaObservacao",
            "salaServicosBelezaObservacaoUpdatedAt",
        ]
        depth = 3
