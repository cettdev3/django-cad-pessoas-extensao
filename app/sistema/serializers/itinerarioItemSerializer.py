# todo/todo_api/serializers.py
from rest_framework import serializers
from ..models.itinerarioItem import ItinerarioItem

class ItinerarioItemSerializer(serializers.ModelSerializer):

    class Meta:
        model = ItinerarioItem
        fields = [
            "id",
            "latitude",
            "longitude",
            "data_hora",
            "endereco",
            "bairro",
            "logradouro",
            "cep",
            "complemento",
            "cidade",
            "escola",
            "itinerario"
        ]
        depth = 3
