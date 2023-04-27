# todo/todo_api/views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions
from django.db import transaction
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
import base64
import uuid
import json
from ..models.galeria import Galeria
from ..models.imagem import Imagem
from ..models.dpEvento import DpEvento
from ..services.alfrescoApi import AlfrescoAPI
from ..serializers.galeriaSerializer import GaleriaSerializer
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

class GaleriaApiView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def get(self, request, *args, **kwargs):
        nome = request.GET.get('nome') if request.GET.get('nome') != "None" else None
        order_by = request.GET.get('order_by') if request.GET.get('order_by') != "None" else None
        galerias = Galeria.objects.prefetch_related('imagem_set')
        eventoId = request.GET.get('dp_evento_id')
        if nome:
            galerias = galerias.filter(nome__icontains=nome)
        if eventoId:
            galerias = galerias.filter(evento__id=eventoId)
        if order_by:
            galerias = galerias.order_by(order_by)
        
        galerias = galerias.all()
        serializer = GaleriaSerializer(galerias, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        data = json.loads(request.body)
        eventoId = data.get('dp_evento_id')
        if not eventoId:
            return Response({'message': 'Evento não informado'}, status=status.HTTP_400_BAD_REQUEST)

        with transaction.atomic():
            galeria = Galeria()
            galeria.nome = data.get('nome')
            galeria.evento = DpEvento.objects.get(id=eventoId)
            galeria.save()

            alfresco = AlfrescoAPI()
            images_data = data.get('imagens', [])
            for image_data in images_data:
                image_description = image_data.get('description', '')

                image_data_url = image_data.get('dataUrl', '')
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
                    descricao=image_data.get("descricao"),
                    galeria=galeria,
                    shared_link=shared_link_url
                )
                imagem.save()
                default_storage.delete(image_path)
        return Response({"id": galeria.id, "nome": galeria.nome}, status=status.HTTP_201_CREATED)

class GaleriaDetailApiView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    
    def get_object(self, fn, object_id):
        try:
            return fn.objects.get(id=object_id)
        except fn.DoesNotExist:
            return None
            
    def get(self, request, galeria_id, *args, **kwargs):
        galeria = self.get_object(Galeria, galeria_id)
        if not galeria:
            return Response(
                {"res": "Não existe galeria com o id informado"},
                status=status.HTTP_400_BAD_REQUEST
            )
        serializer = GaleriaSerializer(galeria)
        print("serializer.data: ", serializer.data)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, galeria_id, *args, **kwargs):
        galeria = self.get_object(Galeria, galeria_id)
        
        if not galeria:
            return Response(
                {"res": "Não existe galeria com o id informado"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        data = {}
        if request.data.get("nome"):
            data["nome"] = request.data.get("nome")

        serializer = GaleriaSerializer(instance=galeria, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, galeria_id, *args, **kwargs):
        galeria = self.get_object(Galeria, galeria_id)
        if not galeria:
            return Response(
                {"res": "Não existe galeria com o id informado"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        with transaction.atomic():
            imagemSet = galeria.imagem_set.all()
            for imagem in imagemSet:
                response = AlfrescoAPI().deleteNode(imagem.id_alfresco)
                imagem.delete()

            galeria.delete()
        return Response(
            {"res": "galeria deletada!"},
            status=status.HTTP_200_OK
        )
