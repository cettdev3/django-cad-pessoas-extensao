# todo/todo_api/serializers.py
from rest_framework import serializers
from ..models.atividadeSection import AtividadeSection
from .atividadeSerializer import AtividadeSerializer

class AtividadeSectionSerializer(serializers.ModelSerializer):
    atividade_set = AtividadeSerializer(many=True, read_only=True)

    class Meta:
        model = AtividadeSection
        fields = [
            "id",
            "nome",
            "order",
            "atividade_set"
        ]
