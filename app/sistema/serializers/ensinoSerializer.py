# todo/todo_api/serializers.py
from rest_framework import serializers
from .dpEventoEnsinoSerializer import DpEventoEnsinoSerializer
from .anexoSerializer import AnexoSerializer
from ..models.ensino import Ensino

class EnsinoSerializer(serializers.ModelSerializer):
    data_inicio = serializers.DateTimeField(format='%Y-%m-%dT%H:%M')
    data_fim = serializers.DateTimeField(format='%Y-%m-%dT%H:%M')
    data_inicio_formatada = serializers.DateField(format='%d/%m/%Y')
    data_fim_formatada = serializers.DateField(format='%d/%m/%Y')
    tipo_formatado = serializers.CharField(read_only=True)
    first_dp_evento = serializers.SerializerMethodField()
    anexo_oficio = AnexoSerializer(read_only=True)
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
            "first_dp_evento",
            "numero_oficio",
            "anexo_oficio",
            "has_credito_social"
        ]
        depth = 2
        
    def get_first_dp_evento(self, obj):
        if not hasattr(obj, 'first_dp_evento'):
            return None
        
        first_dp_evento = obj.first_dp_evento[0] if obj.first_dp_evento else None
        if first_dp_evento:
            return DpEventoEnsinoSerializer(first_dp_evento).data
        return None
