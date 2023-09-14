# todo/todo_api/serializers.py
from rest_framework import serializers
from ..models.membroExecucaoRoles import MembroExecucaoRoles

class MembroExecucaoRoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = MembroExecucaoRoles
        fields = [
            "id",
            "nome",
            "slug"        
        ]
