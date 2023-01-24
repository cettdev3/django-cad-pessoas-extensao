from rest_framework import serializers
from ..models.tipoAtividade import TipoAtividade

class TipoAtividadeSerializer(serializers.ModelSerializer):
    class Meta:
        model = TipoAtividade
        fields = [
            "id",
            "nome",
            "descricao",
            "categoria"
        ]
