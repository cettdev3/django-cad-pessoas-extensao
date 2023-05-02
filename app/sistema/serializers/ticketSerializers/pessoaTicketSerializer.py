# todo/todo_api/serializers.py
from rest_framework import serializers
from ...models.pessoa import Pessoas

class PessoaTicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pessoas
        fields = [
            "id",
            "nome"
        ]
