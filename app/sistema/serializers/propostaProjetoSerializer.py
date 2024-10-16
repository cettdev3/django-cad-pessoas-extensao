# todo/todo_api/serializers.py
from rest_framework import serializers
from ..models.propostaProjeto import PropostaProjeto
from ..serializers.orcamentoSerializer import OrcamentoSerializer

class PropostaProjetoSerializer(serializers.ModelSerializer):
    orcamento = OrcamentoSerializer(read_only=True)
    
    class Meta:
        model = PropostaProjeto
        fields = [
            "id",
            "orcamento",
            "status_menu_label",
            "formato_conteudo_tipo",
            "formato_conteudo_tipo_formatado",
        ]
