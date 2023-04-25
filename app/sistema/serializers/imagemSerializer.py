# todo/todo_api/serializers.py
from rest_framework import serializers
from ..models.imagem import Imagem

class ImagemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Imagem
        fields = [
            "id",
            "id_alfresco",
            "descricao",
            "shared_link",
        ]
