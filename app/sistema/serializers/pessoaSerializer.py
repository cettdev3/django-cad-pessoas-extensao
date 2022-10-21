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
            "sexo",
            "estado_civil",
            "telefone_recado",
            "pis_pasep",
            "data_emissao",
            "nome_mae",
            "nome_pai",
            "tipo_conta",
            "numero_endereco",
            "estado",
            "cursos"
        ]
        depth = 1
