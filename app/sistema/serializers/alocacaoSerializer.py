# todo/todo_api/serializers.py
from rest_framework import serializers
from ..models.alocacao import Alocacao
from ..serializers.dataRemovidaSerializer import DataRemovidaSerializer

class AlocacaoSerializer(serializers.ModelSerializer):
    dataremovida_set = DataRemovidaSerializer(many=True, read_only=True)
    class Meta:
        model = Alocacao
        fields = [
            "id",
            "acaoEnsino",
            "professor",
            "curso",
            "data_inicio",
            "data_fim",
            "status",
            "observacao",
            "bairro",
            "logradouro",
            "cep",
            "complemento",
            "cidade",
            "turnos",
            "aulas_sabado",
            "dataremovida_set",
            "acao",
            "evento",
            "avaliador",
            "bairro",
            "logradouro",
            "cep",
            "complemento",
            "cidade"
        ]
        depth = 2
