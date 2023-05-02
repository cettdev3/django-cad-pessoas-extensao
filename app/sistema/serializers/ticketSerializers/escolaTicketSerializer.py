# todo/todo_api/serializers.py
from rest_framework import serializers
from ...models.escola import Escola

class EscolaTicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Escola
        fields = [
            "id",
            "nome"
        ]
