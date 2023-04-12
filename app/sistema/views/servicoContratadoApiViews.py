# todo/todo_api/views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from ..models.servicoContratado import ServicoContratado
from ..serializers.servicoContratadoSerializer import ServicoContratadoSerializer
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

class ServicoContratadoApiView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def get(self, request, *args, **kwargs):
        print("dentro da rota de servicos contratados")
        servicosContratados = ServicoContratado.objects.all()
        serializer = ServicoContratadoSerializer(servicosContratados, many=True)
        
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        print("dentro da rota de servicos contratados", request.data)
        data = {
            "descricao": request.data.get("descricao"),
            "valor": request.data.get("valor"),
            "data_limite": request.data.get("data_limite"),
        }
        
        serializer = ServicoContratadoSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            print("dados salvos com sucesso", serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ServicoContratadoDetailApiView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    
    def get_object(self, fn, object_id):
        try:
            return fn.objects.get(id=object_id)
        except fn.DoesNotExist:
            return None
            
    def get(self, request, servico_contratado_id, *args, **kwargs):
        servico_contratado = self.get_object(ServicoContratado, servico_contratado_id)
        if not servico_contratado:
            return Response(
                {"res": "Não existe servico contratado com o id informado"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        serializer = ServicoContratadoSerializer(servico_contratado)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, servico_contratado_id, *args, **kwargs):
        servico_contratado = self.get_object(ServicoContratado, servico_contratado_id)
        if not servico_contratado:
            return Response(
                {"res": "Não existe servico contratado com o id informado"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        if request.data.get("descricao"):
            servico_contratado.descricao = request.data.get("descricao")
        if request.data.get("valor"):
            servico_contratado.valor = request.data.get("valor")
        if request.data.get("data_limite"):
            servico_contratado.data_limite = request.data.get("data_limite")

        servico_contratado.save()
        serializer = ServicoContratadoSerializer(servico_contratado)
        
        return Response(serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, servico_contratado_id, *args, **kwargs):
        
        servico_contratado = self.get_object(ServicoContratado, servico_contratado_id)
        if not servico_contratado:
            return Response(
                {"res": "Não existe servico contratado com o id informado"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        servico_contratado.delete()
        return Response(
            {"res": "servico contratado deletado com sucesso"},
            status=status.HTTP_200_OK
        )