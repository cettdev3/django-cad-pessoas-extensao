# todo/todo_api/serializers.py
from rest_framework import serializers
from ..models.dpEvento import DpEvento

class DpEventoTicketSerializer(serializers.ModelSerializer):
    endereco_completo = serializers.CharField(read_only=True)
    data_inicio_formatada = serializers.CharField(read_only=True)
    data_fim_formatada = serializers.CharField(read_only=True)
    tipo_formatado = serializers.CharField(read_only=True)
    
    class Meta:
        model = DpEvento
        fields = [
            "id",
            "tipo",
            "status",
            "data_inicio",
            "data_fim",
            "cidade",
            "endereco_completo",
            "data_inicio_formatada",
            "data_fim_formatada",
            "tipo_formatado",
        ]
        depth = 5
