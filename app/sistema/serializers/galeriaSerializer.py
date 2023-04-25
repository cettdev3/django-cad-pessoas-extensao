# todo/todo_api/serializers.py
from rest_framework import serializers
from ..models.galeria import Galeria
from ..serializers.imagemSerializer import ImagemSerializer

class GaleriaSerializer(serializers.ModelSerializer):
    imagem_set = ImagemSerializer(many=True, read_only=True)
    class Meta:
        model = Galeria
        fields = [
            "id",
            "nome",
            "imagem_set"
        ]
