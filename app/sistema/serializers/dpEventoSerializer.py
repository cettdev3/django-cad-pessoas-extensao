# todo/todo_api/serializers.py
from rest_framework import serializers
from ..models.dpEvento import DpEvento
from ..models.cidade import Cidade

from .membroExecucaoSerializer import MembroExecucaoSerializer

class DpEventoSerializer(serializers.ModelSerializer):
    membroexecucao_set = MembroExecucaoSerializer(many=True, read_only=True)
    endereco_completo = serializers.CharField(read_only=True)
    data_inicio_formatada = serializers.CharField(read_only=True)
    data_inicio_formatada = serializers.CharField(read_only=True)
    
    class Meta:
        model = DpEvento
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
            "acaoEnsino",
            "endereco_completo",
            "data_inicio_formatada",
            "data_fim_formatada",
            "membroexecucao_set"
        ]
        depth = 5
