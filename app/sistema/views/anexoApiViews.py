# todo/todo_api/views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
import base64
import uuid
import json
from ..models.galeria import Galeria
from ..models.imagem import Imagem
from ..models.dpEvento import DpEvento
from ..services.alfrescoApi import AlfrescoAPI
from ..serializers.imagemSerializer import ImagemSerializer
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
# todo/todo_api/views.py
from ..models.anexo import Anexo
from ..serializers.anexoSerializer import AnexoSerializer

class AnexoApiView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    def get_extension_from_mime_type(mime_type):
        mime_type_map = {
            "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet": "xlsx",
            "application/vnd.openxmlformats-officedocument.wordprocessingml.document": "docx",
            "application/vnd.ms-powerpoint.presentation.macroEnabled.12": "pptm",
            # Add more MIME types and their corresponding extensions here as needed
        }

        return mime_type_map.get(mime_type, "")
    
    def get(self, request, *args, **kwargs):
        anexos = Anexo.objects.all()
        serializer = AnexoSerializer(anexos, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        data = json.loads(request.body)
        alfresco = AlfrescoAPI()
        # Process and save the file to Alfresco
        file_data_url = data.get('dataUrl', '')
        file_format, file_str = file_data_url.split(';base64,')
        file_ext = file_format.split('/')[-1]
        mime_type = file_format.split(':')[1]
        file_content_bytes = base64.b64decode(file_str)
        file_content = ContentFile(file_content_bytes)
        file_ext = data.get("nome").split('.')[-1]
        file_name = f'{uuid.uuid4()}.{file_ext}'
        file_path = default_storage.save(f'tmp/{file_name}', file_content)

        alfrescoNode = alfresco.createNode(file_path, "cm:content", file_name)
        shared_link = alfresco.createSharedLink(alfrescoNode.entry_id)
        shared_link = json.loads(shared_link)
        entry = shared_link['entry']
        node_id = entry['id']
        alfresco_base_url = "https://docs.cett.org.br/alfresco/api/-default-/public/alfresco/versions/1"
        shared_link_url = f"{alfresco_base_url}/shared-links/{node_id}/content"

        anexo = Anexo(
            nome=data.get("nome"),
            fonte=data.get("fonte"),
            descricao=data.get("descricao"),
            mime_type=mime_type,
            model=data.get("model"),
            id_model=data.get("id_model"),
            id_alfresco=alfrescoNode.entry_id,
            shared_link=shared_link_url
        )
        anexo.save()
        default_storage.delete(file_path)
        serializer = AnexoSerializer(anexo)

        return Response(serializer.data, status=status.HTTP_201_CREATED)


class AnexoDetailApiView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    
    def get_object(self, fn, object_id):
        try:
            return fn.objects.get(id=object_id)
        except fn.DoesNotExist:
            return None
            
    def get(self, request, anexo_id, *args, **kwargs):
        anexo = self.get_object(Anexo, anexo_id)
        if not anexo:
            return Response(
                {"res": "Não existe anexo com o id informado"},
                status=status.HTTP_400_BAD_REQUEST
            )
        serializer = AnexoSerializer(anexo)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, anexo_id, *args, **kwargs):
        anexo = self.get_object(Anexo, anexo_id)
        if not anexo:
            return Response(
                {"res": "Não existe anexo com o id informado"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        data = {}
        
        if request.data.get("nome"):
            data["nome"] = request.data.get("nome")
        if request.data.get("descricao"):
            data["descricao"] = request.data.get("descricao")
        if request.data.get("fonte"):
            data["fonte"] = request.data.get("fonte")
        

        serializer = AnexoSerializer(instance=anexo, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, anexo_id, *args, **kwargs):
        anexo = self.get_object(Anexo, anexo_id)
        if not anexo:
            return Response(
                {"res": "Não existe anexo com o id informado"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        alfresco = AlfrescoAPI()
        response = alfresco.deleteNode(anexo.id_alfresco)
        if response.status_code != 204:
            return Response(
                {"res": "Erro ao deletar anexo no alfresco"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        anexo.delete()
        return Response(
            {"res": "Anexo deletado!"},
            status=status.HTTP_200_OK
        )
