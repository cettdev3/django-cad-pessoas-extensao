# todo/todo_api/serializers.py
from rest_framework import serializers
from ..models.itinerario import Itinerario
from .itinerarioItemSerializer import ItinerarioItemSerializer

class ItinerarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Itinerario
        fields = [
            "id",
            "color",
            "itinerarioitem_set"
        ]
        depth = 3
