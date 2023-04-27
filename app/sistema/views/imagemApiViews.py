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

class ImagemApiView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def get(self, request, *args, **kwargs):
        imagens = Imagem.objects.all()
        serializer = ImagemSerializer(imagens, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        data = json.loads(request.body)
        print(data)
        galeria_id = data.get('galeria_id')
        if not galeria_id:
            return Response({'message': 'Galeria não informado'}, status=status.HTTP_400_BAD_REQUEST)
        
        galeria = Galeria.objects.get(id=galeria_id)

        alfresco = AlfrescoAPI()
        
        image_description = data.get('description', '')

        # Process and save the image file to Alfresco
        image_data_url = data.get('dataUrl', '')
        image_format, image_str = image_data_url.split(';base64,')
        image_ext = image_format.split('/')[-1]
        image_content_bytes = base64.b64decode(image_str)
        image_content = ContentFile(image_content_bytes)
        image_name = f'{uuid.uuid4()}.jpg'
        image_path = default_storage.save(f'tmp/{image_name}', image_content)

        alfrescoNode = alfresco.createNode(image_path, "cm:content", image_name)
        shared_link = alfresco.createSharedLink(alfrescoNode.entry_id)
        shared_link = json.loads( shared_link )
        entry = shared_link['entry']
        node_id = entry['id']
        alfresco_base_url = "https://docs.cett.org.br/alfresco/api/-default-/public/alfresco/versions/1"
        shared_link_url = f"{alfresco_base_url}/shared-links/{node_id}/content"

        imagem = Imagem(
            id_alfresco=alfrescoNode.entry_id,
            descricao=data.get("descricao"),
            galeria=galeria,
            shared_link=shared_link_url
        )
        imagem.save()
        default_storage.delete(image_path)
        serializer = ImagemSerializer(imagem)

        return Response(serializer.data, status=status.HTTP_201_CREATED)

class ImagemDetailApiView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    
    def get_object(self, fn, object_id):
        try:
            return fn.objects.get(id=object_id)
        except fn.DoesNotExist:
            return None
            
    def get(self, request, imagem_id, *args, **kwargs):
        imagem = self.get_object(Galeria, imagem_id)
        if not imagem:
            return Response(
                {"res": "Não existe imagem com o id informado"},
                status=status.HTTP_400_BAD_REQUEST
            )
        serializer = ImagemSerializer(imagem)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, imagem_id, *args, **kwargs):
        imagem = self.get_object(Imagem, imagem_id)
        if not imagem:
            return Response(
                {"res": "Não existe imagem com o id informado"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        data = {}
        if request.data.get("descricao"):
            data["descricao"] = request.data.get("descricao")

        serializer = ImagemSerializer(instance=imagem, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, imagem_id, *args, **kwargs):
        imagem = self.get_object(Imagem, imagem_id)
        if not imagem:
            return Response(
                {"res": "Não existe imagem com o id informado"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        alfresco = AlfrescoAPI()
        response = alfresco.deleteNode(imagem.id_alfresco)
        if response.status_code != 204:
            return Response(
                {"res": "Erro ao deletar imagem no alfresco"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        imagem.delete()
        return Response(
            {"res": "imagem deletada!"},
            status=status.HTTP_200_OK
        )
