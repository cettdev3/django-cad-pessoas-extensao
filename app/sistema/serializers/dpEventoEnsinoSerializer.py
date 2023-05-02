# todo/todo_api/serializers.py
from rest_framework import serializers
from ..models.dpEvento import DpEvento
class DpEventoEnsinoSerializer(serializers.ModelSerializer):    
    class Meta:
        model = DpEvento
        fields = [
            "id",
        ]
