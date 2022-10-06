# todo/todo_api/serializers.py
from rest_framework import serializers
from ..models.pessoa import Pessoas

class PessoaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pessoas
        fields = [
            "id",
            "email",
            "nome",
            "data_nascimento",
            "telefone",
            "cpf",
            "rg",
            "orgao_emissor",
            "endereco",
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
