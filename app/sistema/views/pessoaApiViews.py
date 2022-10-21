# todo/todo_api/views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import Q
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
        cpf = request.GET.get('cpf')
        pessoas = Pessoas.objects
        if cpf:
            cpfNaoFormatado = cpf.replace('.', '').replace('-','')
            pessoas = pessoas.filter(Q(cpf=cpf)|Q(cpf=cpfNaoFormatado))
        pessoas = pessoas.all()
        serializer = PessoaSerializer(pessoas, many=True)
        return Response(serializer.data, status=st.HTTP_200_OK)

    # 2. Create
    def post(self, request, *args, **kwargs):
        sexo = request.data.get('sexo')
        telefone_recado = request.data.get('telefone_recado')
        pis_pasep = request.data.get('pis_pasep')
        if request.data.get("data_emissao"):
            data_emissao = request.data.get("data_emissao")
        else: data_emissao = None
        estado_civil = request.data.get("estado_civil")
        nome_mae = request.data.get('nome_mae')
        nome_pai = request.data.get('nome_pai')
        tipo_conta = request.data.get('tipo_conta')
        numero_endereco = request.data.get('numero_endereco')
        estado = request.data.get('estado')
        cursos =  request.data.get('cursos')
        nome = request.data.get('nome')
        email = request.data.get('email')
        data_nascimento = request.data.get("data_nascimento")
        telefone = request.data.get("telefone")
        cpf = request.data.get("cpf")
        rg = request.data.get("rg")
        orgao_emissor = request.data.get("orgao_emissor")
        cidade = request.data.get("cidade")
        bairro = request.data.get("bairro")
        rua = request.data.get("rua")
        cep = request.data.get("cep")
        complemento = request.data.get("complemento")
        cargo = request.data.get("cargo")
        banco = request.data.get("banco")
        agencia = request.data.get("agencia")
        conta = request.data.get("conta")
        pix = request.data.get("pix")
        tipo = request.data.get("tipo")
        qtd_contratacoes = request.data.get("qtd_contratacoes")
        user_camunda = request.data.get("user_camunda")


        pessoa = Pessoas.objects.create(
            nome = nome,
            email = email,
            estado_civil = estado_civil,
            data_nascimento = data_nascimento,
            telefone = telefone,
            cpf = cpf,
            rg = rg,
            orgao_emissor = orgao_emissor,
            cidade = cidade,
            bairro = bairro,
            rua = rua,
            sexo = sexo,
            telefone_recado = telefone_recado,
            pis_pasep = pis_pasep,
            data_emissao = data_emissao,
            nome_mae = nome_mae,
            nome_pai = nome_pai,
            tipo_conta = tipo_conta,
            numero_endereco = numero_endereco,
            estado = estado,
            complemento = complemento,
            cep = cep,
            cargo = cargo,
            banco = banco,
            agencia = agencia,
            conta = conta,
            pix = pix,
            tipo = tipo,
            qtd_contratacoes = qtd_contratacoes,
            user_camunda = user_camunda,
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

        requestCursos = request.data.get("cursos")
        if requestCursos:
            cursosIds = requestCursos
            cursos = []
            for cursoId in cursosIds:
                if type(cursoId) == dict:
                    cursoId = cursoId["id"]    
                curso = self.get_object(Curso, cursoId)
                if not curso:
                    return Response(
                        {"res": f"Não existe curso com o id informado: {str(cursoId)}"}, 
                        status=st.HTTP_400_BAD_REQUEST
                    )
                cursos.append(curso)
           
            pessoa.cursos.set(cursos)
        elif type(requestCursos) is list:
            pessoa.cursos.set([])

        if request.data.get("nome"):
            pessoa.nome = request.data.get("nome")
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
        if request.data.get("cidade"):
            pessoa.cidade = request.data.get("cidade")
        if request.data.get("bairro"):
            pessoa.bairro = request.data.get("bairro")
        if request.data.get("rua"):
            pessoa.rua = request.data.get("rua")
        if request.data.get("cep"):
            pessoa.cep = request.data.get("cep")
        if request.data.get("complemento"):
            pessoa.complemento = request.data.get("complemento")
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
        if request.data.get("sexo"):
            pessoa.sexo = request.data.get("sexo")
        if request.data.get("estado_civil"):
            pessoa.estado_civil = request.data.get("estado_civil")
        if request.data.get("telefone_recado"):
            pessoa.telefone_recado = request.data.get("telefone_recado")
        if request.data.get("pis_pasep"):
            pessoa.pis_pasep = request.data.get("pis_pasep")
        data_emissao = request.data.get("data_emissao")
        if data_emissao and len(data_emissao) > 0:
            pessoa.data_emissao = request.data.get("data_emissao")
        if request.data.get("nome_mae"):
            pessoa.nome_mae = request.data.get("nome_mae")
        if request.data.get("nome_pai"):
            pessoa.nome_pai = request.data.get("nome_pai")
        if request.data.get("tipo_conta"):
            pessoa.tipo_conta = request.data.get("tipo_conta")
        if request.data.get("numero_endereco"):
            pessoa.numero_endereco = request.data.get("numero_endereco")
        if request.data.get("estado"):
            pessoa.estado = request.data.get("estado")
        
                
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