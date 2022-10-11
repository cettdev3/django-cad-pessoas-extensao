# todo/todo_api/serializers.py
from rest_framework import serializers
from ..models.curso import Curso

class CursoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Curso
        fields = [
            "id",
            "nome"
        ]
