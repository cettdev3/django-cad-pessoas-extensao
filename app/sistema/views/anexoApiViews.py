# todo/todo_api/views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import json
from ..services.alfrescoApi import AlfrescoAPI
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from ..models.anexo import Anexo
from ..serializers.anexoSerializer import AnexoSerializer
from ..services.anexoService import AnexoService
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
        anexoService = AnexoService()
        anexo = anexoService.create_anexo(data)
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
