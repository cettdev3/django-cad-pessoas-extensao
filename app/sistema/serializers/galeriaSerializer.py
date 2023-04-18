# todo/todo_api/serializers.py
from rest_framework import serializers
from ..models.galeria import Galeria

class GaleriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Galeria
        fields = [
            "id",
            "nome"
        ]
