# todo/todo_api/serializers.py
from rest_framework import serializers
from ..models.turno import Turno

class TurnoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Turno
        fields = [
            "id",
            "nome",
            "carga_horaria"
        ]
