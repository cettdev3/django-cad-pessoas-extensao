# todo/todo_api/serializers.py
from datetime import datetime
from rest_framework import serializers
from ..models.pessoa import Pessoas

class PessoaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pessoas
        fields = [
            "id",
            "email",
            "nome",
            "data_nascimento_formatted",
            "telefone",
            "cpf",
            "rg",
            "orgao_emissor",
            "cidade",
            "bairro",
            "rua",
            "cep",
            "complemento",
            "cep",
            "cargo",
            "banco",
            "agencia",
            "conta",
            "pix",
            "tipo",
            "qtd_contratacoes",
            "user_camunda",
            "cursos"
        ]
        depth = 1
