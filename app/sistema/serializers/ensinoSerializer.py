# todo/todo_api/serializers.py
from rest_framework import serializers

from .enderecoSerializer import EnderecoSerializer

from ..models.endereco import Endereco
from ..models.ensino import Ensino

class EnsinoSerializer(serializers.ModelSerializer):
    data_inicio = serializers.DateTimeField(format='%Y-%m-%dT%H:%M')
    data_fim = serializers.DateTimeField(format='%Y-%m-%dT%H:%M')
    data_inicio_formatada = serializers.DateField(format='%d/%m/%Y')
    data_fim_formatada = serializers.DateField(format='%d/%m/%Y')
    tipo_formatado = serializers.CharField(read_only=True)
    class Meta:
        model = Ensino
        fields = [
            "id",
            "data_inicio",
            "data_fim",
            "observacao",
            "tipo",
            "process_instance",
            "status",
            "endereco",
            "status_class",
            "etapa",
            "logradouro",
            "complemento",
            "bairro",
            "cidade",
            "cep",
            "escola",
            "data_inicio_formatada",
            "data_fim_formatada",
            "tipo_formatado",
        ]
        depth = 2
        
