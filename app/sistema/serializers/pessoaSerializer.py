# todo/todo_api/serializers.py
from datetime import datetime
from rest_framework import serializers
from ..models.pessoa import Pessoas
from ..serializers.alocacaoSerializer import AlocacaoSerializer

class PessoaSerializer(serializers.ModelSerializer):
    count_alocacao = serializers.IntegerField(initial=0, allow_null=True)
    alocacao_set = AlocacaoSerializer(many=True, read_only=True)
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
            "id_protocolo",
            "numero_endereco",
            "estado",
            "cursos",
            "alocacao_set",
            "count_alocacao"
        ]
        depth = 2
