# todo/todo_api/serializers.py
from rest_framework import serializers
from ..models.dpEvento import DpEvento
from ..models.cidade import Cidade
from .escolaSerializer import EscolaSerializer
from .membroExecucaoSerializer import MembroExecucaoSerializer

class DpEventoSerializer(serializers.ModelSerializer):
    membroexecucao_set = MembroExecucaoSerializer(many=True, read_only=True)
    endereco_completo = serializers.CharField(read_only=True)
    data_inicio_formatada = serializers.CharField(read_only=True)
    data_fim_formatada = serializers.CharField(read_only=True)
    tipo_formatado = serializers.CharField(read_only=True)
    escolas = EscolaSerializer(many=True, read_only=True)
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
            "escolas",
            "acaoEnsino",
            "endereco_completo",
            "data_inicio_formatada",
            "data_fim_formatada",
            "tipo_formatado",
            "membroexecucao_set",
            "membro_execucao_status",
            "horarioInicio",
            "horarioFim",
            "edicao"
        ]
        depth = 5
