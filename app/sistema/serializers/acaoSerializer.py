# todo/todo_api/serializers.py
from rest_framework import serializers
from ..models.acao import Acao
from ..models.cidade import Cidade

from .membroExecucaoSerializer import MembroExecucaoSerializer

class AcaoSerializer(serializers.ModelSerializer):
    membroexecucao_set = MembroExecucaoSerializer(many=True, read_only=True)
    endereco_completo = serializers.CharField()
    data_inicio_formatada = serializers.CharField()
    data_inicio_formatada = serializers.CharField()
    class Meta:
        model = Acao
        fields = [
            "id",
            "tipo",
            "process_instance",
            "variaveis",
            "status",
            "descricao",
            "data_inicio",
            "data_fim",
            "bairro",
            "logradouro",
            "cep",
            "complemento",
            "cidade",
            "escola",
            "endereco_completo",
            "data_inicio_formatada",
            "data_fim_formatada",
            "membroexecucao_set"
        ]
        depth = 10
