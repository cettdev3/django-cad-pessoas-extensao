# todo/todo_api/serializers.py
from rest_framework import serializers
from ..models.comentario import Comentario

class ComentarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comentario
        fields = [
            "id",
            "conteudo",
            "autor",
            "proposta_projeto",
            "created_at",
            "created_at_formatado"
        ]