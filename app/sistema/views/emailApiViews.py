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
        email_type = data.get('email_type')
        model_id = data.get('model_id')
        proposta_projeto = PropostaProjeto.objects.get(id=model_id)
        try:
            success = PropostaSubmetidaEmail(proposta_projeto).send()
        except Exception as e:
            print(e)
            return Response({"res": "Erro ao enviar email"}, status=status.HTTP_400_BAD_REQUEST)

        return Response({"res": "Email enviado com sucesso"}, status=status.HTTP_200_OK)
