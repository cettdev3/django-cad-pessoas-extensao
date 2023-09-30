# todo/todo_api/serializers.py
from rest_framework import serializers
from ..models.anexo import Anexo

class AnexoSerializer(serializers.ModelSerializer):
    extension = serializers.SerializerMethodField()
    tipo_anexo_formatado = serializers.SerializerMethodField()
    class Meta:
        model = Anexo
        fields = [
            "id",
            "fonte",
            "nome",
            "descricao",
            "mime_type",
            "model",
            "id_model",
            "id_alfresco",
            "shared_link",
            "extension",
            "tipo",
            "tipo_anexo_formatado"
        ]

    def get_extension(self, obj):
        nome = obj["nome"] if type(obj) == dict else obj.nome
        if nome:
            ext = nome.split('.')[-1]
            if ext in ['pdf']:
                return "pdf"
            elif ext in ['doc', 'docx']:
                return "doc"
            elif ext in ['xls', 'xlsx']:
                return "xls"
            elif ext in ['ppt', 'pptx', 'pptm']:
                return "ppt"
            elif ext in ['jpg', 'jpeg', 'png', 'gif', "webp"]:
                return "img"
            else:
                return "file"
        else:
            return "file"

    def get_tipo_anexo_formatado(self, obj):
        if not obj['tipo']:
            return None
        if  obj['tipo'] == Anexo.ANEXO_TIPO_RELATORIO_PROFESSOR:
            return "Relatório do(a) professor(a)"
        elif  obj['tipo'] == Anexo.ANEXO_TIPO_LISTA_PRESENCA:
            return "Lista de presença"
        elif  obj['tipo'] == Anexo.ANEXO_TIPO_OUTRO:
            return "Outro"