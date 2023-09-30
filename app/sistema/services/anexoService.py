from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
import base64
import json
import uuid

from .alfrescoApi import AlfrescoAPI
from ..models import Anexo
from ..serializers import AnexoSerializer

class AnexoService:
    def __init__(self):
        self.alfresco = AlfrescoAPI()

    def create_anexo(self, data):
        file_data_url = data.get('dataUrl', '')
        file_format, file_str = file_data_url.split(';base64,')
        file_ext = file_format.split('/')[-1]
        mime_type = file_format.split(':')[1]
        file_content_bytes = base64.b64decode(file_str)
        file_content = ContentFile(file_content_bytes)
        file_ext = data.get("nome").split('.')[-1]
        file_name = f'{uuid.uuid4()}.{file_ext}'
        file_path = default_storage.save(f'tmp/{file_name}', file_content)

        alfrescoNode = self.alfresco.createNode(file_path, "cm:content", file_name)
        shared_link = self.alfresco.createSharedLink(alfrescoNode.entry_id)
        shared_link = json.loads(shared_link)
        entry = shared_link['entry']
        node_id = entry['id']
        alfresco_base_url = "https://docs.cett.org.br/alfresco/api/-default-/public/alfresco/versions/1"
        shared_link_url = f"{alfresco_base_url}/shared-links/{node_id}/content"
        print("tipo do anexo: ", data.get("tipo"))
        anexo = Anexo(
            nome=data.get("nome"),
            fonte=data.get("fonte"),
            descricao=data.get("descricao"),
            mime_type=mime_type,
            model=data.get("model"),
            id_model=data.get("id_model"),
            id_alfresco=alfrescoNode.entry_id,
            shared_link=shared_link_url,
            tipo=data.get("tipo")
        )
        
        anexo.save()
        default_storage.delete(file_path)
        return anexo