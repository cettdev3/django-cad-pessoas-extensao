# todo/todo_api/views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status as st
from rest_framework import permissions
from ..models.pessoa import Pessoas
from ..models.curso import Curso
from ..serializers.pessoaSerializer import PessoaSerializer

class PessoaApiView(APIView):
    # add permission to check if user is authenticated
    permission_classes = [permissions.AllowAny]

    # 1. List all
    def get(self, request, *args, **kwargs):
        todos = Pessoas.objects.all()
        print("dados retornados",todos)
        serializer = PessoaSerializer(todos, many=True)
        return Response(serializer.data, status=st.HTTP_200_OK)

    # 2. Create
    def post(self, request, *args, **kwargs):
        cursos =  request.data.get('cursos')
        nome = request.data.get('nome')
        email = request.data.get('email')

        pessoa = Pessoas.objects.create(
            nome = nome,
            email = email
        )
        pessoa.cursos.add(*cursos)
        serializer = PessoaSerializer(pessoa)
        return Response(serializer.data, status=st.HTTP_201_CREATED)

        # return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
class PessoaDetailApiView(APIView):
    def get_object(self, fn, object_id):
        try:
            return fn.objects.get(id=object_id)
        except fn.DoesNotExist:
            return None
            
    def get(self, request, pessoa_id, *args, **kwargs):

        pessoa = self.get_object(Pessoas, pessoa_id)
        if not pessoa:
            return Response(
                {"res": "Não existe pessoa cadastrada com o id informado"},
                status=st.HTTP_400_BAD_REQUEST
            )

        serializer = PessoaSerializer(pessoa)
        return Response(serializer.data, status=st.HTTP_200_OK)

    def put(self, request, pessoa_id, *args, **kwargs):
        pessoa = self.get_object(Pessoas, pessoa_id)
        if not pessoa:
                return Response(
                    {"res": "Não existe pessoa cadastrada com o id informado"}, 
                    status=st.HTTP_400_BAD_REQUEST
                )
        if request.data.get("cursos"):
            cursosIds = request.data.get("cursos")
            cursos = []
            for cursoId in cursosIds:
                curso = self.get_object(Curso, cursoId)
                if not curso:
                    return Response(
                        {"res": f"Não existe curso com o id informado: {str(cursoId)}"}, 
                        status=st.HTTP_400_BAD_REQUEST
                    )
                cursos.append(curso)
           
            pessoa.cursos.set(cursos)
        else:
            pessoa.cursos.set([])

        if request.data.get("nome"):
            pessoa.evento = request.data.get("nome")
        if request.data.get("email"):
            pessoa.email = request.data.get("email")
        if request.data.get("data_nascimento"):
            pessoa.data_nascimento = request.data.get("data_nascimento")
        if request.data.get("telefone"):
            pessoa.telefone = request.data.get("telefone")
        if request.data.get("cpf"):
            pessoa.cpf = request.data.get("cpf")
        if request.data.get("rg"):
            pessoa.rg = request.data.get("rg")
        if request.data.get("orgao_emissor"):
            pessoa.orgao_emissor = request.data.get("orgao_emissor")
        if request.data.get("endereco"):
            pessoa.endereco = request.data.get("endereco")
        if request.data.get("cep"):
            pessoa.cep = request.data.get("cep")
        if request.data.get("cargo"):
            pessoa.cargo = request.data.get("cargo")
        if request.data.get("banco"):
            pessoa.banco = request.data.get("banco")
        if request.data.get("agencia"):
            pessoa.agencia = request.data.get("agencia")
        if request.data.get("conta"):
            pessoa.conta = request.data.get("conta")
        if request.data.get("pix"):
            pessoa.pix = request.data.get("pix")
        if request.data.get("tipo"):
            pessoa.tipo = request.data.get("tipo")
        if request.data.get("qtd_contratacoes"):
            pessoa.qtd_contratacoes = request.data.get("qtd_contratacoes")
        if request.data.get("user_camunda"):
            pessoa.user_camunda = request.data.get("user_camunda")
        
                
        pessoa.save()
        serializer = PessoaSerializer(pessoa)
        
        return Response(serializer.data, status=st.HTTP_200_OK)

    def delete(self, request, pessoa_id, *args, **kwargs):
        
        pessoa = self.get_object(Pessoas, pessoa_id)
        if not pessoa:
            return Response(
                {"res": "Não existe pessoa com o id informado"}, 
                status=st.HTTP_400_BAD_REQUEST
            )
        pessoa.delete()
        return Response(
            {"res": "pessoa deletada!"},
            status=st.HTTP_200_OK
        )