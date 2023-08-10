# todo/todo_api/views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from ..models.propostaProjeto import PropostaProjeto
from sistema.emailtemplates.propostaSubmetidaEmail import PropostaSubmetidaEmail

class EmailApiView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication, JWTAuthentication]

    def get_object(self, fn, object_id):
        try:
            return fn.objects.get(id=object_id)
        except fn.DoesNotExist:
            return None

    def post(self, request, *args, **kwargs):
        data = request.data
        titulo_projeto = data.get('titulo_projeto')
        proposta_url = data.get('proposta_url')
        nome_proponente = data.get('nome_proponente')
        try:
            success = PropostaSubmetidaEmail(
                titulo_projeto=titulo_projeto,
                proposta_url=proposta_url,
                nome_proponente=nome_proponente
            ).send()
        except Exception as e:
            print(e)
            return Response({"res": "Erro ao enviar email"}, status=status.HTTP_400_BAD_REQUEST)

        return Response({"res": "Email enviado com sucesso"}, status=status.HTTP_200_OK)
