# todo/todo_api/serializers.py
from rest_framework import serializers
from ..models.anexo import Anexo

class AnexoSerializer(serializers.ModelSerializer):
    extension = serializers.SerializerMethodField()

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
            "extension"
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