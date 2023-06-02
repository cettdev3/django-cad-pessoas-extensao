# todo/todo_api/serializers.py
from rest_framework import serializers
from ..models.atividadeCategoria import AtividadeCategoria

class AtividadeCategoriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = AtividadeCategoria
        fields = [
            "id",
            "name",
            "description",
            "badge",
            "slug",
        ]