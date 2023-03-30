# todo/todo_api/serializers.py
from rest_framework import serializers
from ..models.dataRemovida import DataRemovida

class DataRemovidaSerializer(serializers.ModelSerializer):
    class Meta:
        model = DataRemovida
        fields = [
            "id",
            "date",
            "date_formatted",
        ]
