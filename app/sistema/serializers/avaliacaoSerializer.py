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
        ]
        depth = 3
