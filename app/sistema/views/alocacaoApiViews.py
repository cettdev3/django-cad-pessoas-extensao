# todo/todo_api/views.py
from datetime import datetime
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status as st
from django.db import transaction

from ..models.alocacao import Alocacao
from ..models.pessoa import Pessoas
from ..models.cidade import Cidade
from ..models.evento import Evento
from ..models.curso import Curso
from ..models.dataRemovida import DataRemovida
from ..serializers.alocacaoSerializer import AlocacaoSerializer
from ..serializers.pessoaSerializer import PessoaSerializer
from ..serializers.eventoSerializer import EventoSerializer
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

class AlocacaoApiView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def get_object(self, fn, object_id):
        try:
            return fn.objects.get(id=object_id)
        except fn.DoesNotExist:
            return None

    def get(self, request, *args, **kwargs):
        alocacoes = Alocacao.objects.prefetch_related("dataremovida_set").all()
        serializer = AlocacaoSerializer(alocacoes, many=True)
        return Response(serializer.data, status=st.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        evento = None
        professor = None
        curso = None
        
        if isinstance(request.data, list):
            alocacoesCriadas = []
            with transaction.atomic():
                for alocacaoData in request.data:
                    evento = None
                    professor = None
                    curso = None
                    logradouro = None
                    complemento = None
                    bairro = None
                    cidade = None
                    cep = None
                    aulas_sabado = False
                    
                    if "curso_id" in alocacaoData:
                        curso = self.get_object(Curso, alocacaoData["curso_id"])
                        if not curso:
                            return Response(
                                {"res": "Não existe curso com o id informado"}, 
                                status=st.HTTP_400_BAD_REQUEST
                            )
                    if alocacaoData["evento_id"]:
                        evento = self.get_object(Evento, alocacaoData["evento_id"])
                        if not evento:
                            return Response(
                                {"res": "Não existe evento com o id informado"}, 
                                status=st.HTTP_400_BAD_REQUEST
                            )
                    if alocacaoData["professor_id"]:
                        professor = self.get_object(Pessoas, alocacaoData["professor_id"])
                        if not professor:
                            return Response(
                                {"res": "Não existe professor com o id informado"}, 
                                status=st.HTTP_400_BAD_REQUEST
                            )
                    data_inicio = None
                    data_fim = None
                    if alocacaoData["data_inicio"]:
                        data_inicio = datetime.strptime(alocacaoData["data_inicio"], "%Y-%m-%d").date()
                    if alocacaoData["data_fim"]:
                        data_fim = datetime.strptime(alocacaoData["data_fim"], "%Y-%m-%d").date()
                    status = alocacaoData["status"] if "status" in alocacaoData else None
                    observacao = alocacaoData["observacao"] if "observacao" in alocacaoData else None
                    if alocacaoData["logradouro"]:
                        logradouro = alocacaoData["logradouro"]
                    if alocacaoData["complemento"]:
                        complemento = alocacaoData["complemento"]
                    if alocacaoData["bairro"]:
                        bairro = alocacaoData["bairro"]
                    if alocacaoData["cidade_id"]:
                        cidade = self.get_object(Cidade, alocacaoData["cidade_id"])
                        if not cidade:
                            return Response(
                                {"res": "Não existe evento com o id informado"}, 
                                status=str.HTTP_400_BAD_REQUEST
                            )
                        cidade = cidade
                    if alocacaoData["cep"]:
                        cep = alocacaoData["cep"]
                    
                    if alocacaoData["aulas_sabado"]:
                        aulas_sabado = alocacaoData["aulas_sabado"]

                    alocacao = Alocacao.objects.create(
                        data_inicio = data_inicio,
                        data_fim = data_fim,
                        observacao = observacao,
                        status = status,
                        evento = evento,
                        professor = professor,
                        curso = curso,
                        logradouro = logradouro,
                        complemento = complemento,
                        bairro = bairro,
                        cidade = cidade,
                        cep = cep,
                        aulas_sabado = aulas_sabado
                    )

                    turnos = alocacaoData["turnos"]
                    if turnos:
                        alocacao.turnos.add(*turnos)
                    
                    datasRemovidas = alocacaoData["datas_removidas"]
                    if datasRemovidas:
                        for dataRemovida in datasRemovidas:
                            DataRemovida.objects.create(
                                date = datetime.strptime(dataRemovida, "%Y-%m-%d").date(),
                                alocacao = alocacao
                            )

                    alocacaoSerializer = AlocacaoSerializer(alocacao)
                    alocacoesCriadas.append(alocacaoSerializer.data)
            return Response(alocacoesCriadas, status=st.HTTP_201_CREATED)
        else:
            with transaction.atomic():
                if request.data.get("evento_id"):
                    evento = self.get_object(Evento, request.data.get("evento_id"))
                    if not evento:
                        return Response(
                            {"res": "Não existe evento com o id informado"}, 
                            status=st.HTTP_400_BAD_REQUEST
                        )
                if request.data.get("curso_id"):
                    curso = self.get_object(Curso, request.data.get("curso_id"))
                    if not curso:
                        return Response(
                            {"res": "Não existe curso com o id informado"}, 
                            status=st.HTTP_400_BAD_REQUEST
                        )
                if request.data.get("professor_id"):
                    professor = self.get_object(Pessoas, request.data.get("professor_id"))
                    if not professor:
                        return Response(
                            {"res": "Não existe professor com o id informado"}, 
                            status=st.HTTP_400_BAD_REQUEST
                        )
                
                data_inicio = None
                data_fim = None
                logradouro = None
                complemento = None
                bairro = None
                cidade = None
                cep = None
                aulas_sabado = False

                if request.data.get("data_inicio"):
                    data_inicio = datetime.strptime(request.data.get("data_inicio"), "%Y-%m-%d").date()
                if request.data.get("data_fim"):
                    data_fim = datetime.strptime(request.data.get("data_fim"), "%Y-%m-%d").date()
                status = request.data.get("status") 
                observacao = request.data.get("observacao") 

                if request.data.get("logradouro"):
                    logradouro = request.data.get("logradouro")
                if request.data.get("complemento"):
                    complemento = request.data.get("complemento")
                if request.data.get("bairro"):
                    bairro = request.data.get("bairro")
                if request.data.get("cidade_id"):
                    cidade = self.get_object(Cidade, request.data.get("cidade_id"))
                    if not cidade:
                        return Response(
                            {"res": "Não existe evento com o id informado"}, 
                            status=str.HTTP_400_BAD_REQUEST
                        )
                    cidade = cidade
                if request.data.get("cep"):
                    cep = request.data.get("cep")

                if request.data.get("aulas_sabado"):
                    aulas_sabado = request.data.get("aulas_sabado")

                alocacao = Alocacao.objects.create(
                    data_inicio = data_inicio,
                    data_fim = data_fim,
                    observacao = observacao,
                    status = status,
                    evento = evento,
                    professor = professor,
                    curso = curso,
                    logradouro = logradouro,
                    complemento = complemento,
                    bairro = bairro,
                    cidade = cidade,
                    cep = cep,
                    aulas_sabado = aulas_sabado,
                )
                
                if request.data.get("turnos"):
                    turnos = request.data.get("turnos")
                    alocacao.turnos.add(*turnos)
                
                datasRemovidas = alocacaoData["datas_removidas"]
                if datasRemovidas:
                    for dataRemovida in datasRemovidas:
                        DataRemovida.objects.create(
                            date = datetime.strptime(dataRemovida, "%Y-%m-%d").date(),
                            alocacao = alocacao
                        )
                        
                alocacaoSerializer = AlocacaoSerializer(alocacao)
            return Response(alocacaoSerializer.data, status=st.HTTP_201_CREATED)

class AlocacaoDetailApiView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def get_object(self, fn, object_id):
        try:
            return fn.objects.get(id=object_id)
        except fn.DoesNotExist:
            return None
            
    def get(self, request, alocacao_id, *args, **kwargs):

        alocacao = self.get_object(Alocacao, alocacao_id)
        if not alocacao:
            return Response(
                {"res": "Não existe alocaçao com o id informado"},
                status=st.HTTP_400_BAD_REQUEST
            )

        serializer = AlocacaoSerializer(alocacao)
        return Response(serializer.data, status=st.HTTP_200_OK)

    def put(self, request, alocacao_id, *args, **kwargs):
        alocacao = self.get_object(Alocacao, alocacao_id)
        if not alocacao:
                return Response(
                    {"res": "Não existe alocação com o id informado"}, 
                    status=st.HTTP_400_BAD_REQUEST
                )
        
        if request.data.get("curso_id"):
            curso = self.get_object(Curso, request.data.get("curso_id"))
            if not curso:
                return Response(
                    {"res": "Não existe curso com o id informado"}, 
                    status=st.HTTP_400_BAD_REQUEST
                )
            alocacao.curso = curso
        else:
            alocacao.curso = None

        if request.data.get("evento_id"):
            evento = self.get_object(Evento, request.data.get("evento_id"))
            if not evento:
                return Response(
                    {"res": "Não existe evento com o id informado"}, 
                    status=st.HTTP_400_BAD_REQUEST
                )
            alocacao.evento = evento
        else:
            alocacao.evento = None

        if request.data.get("professor_id"):
            professor = self.get_object(Pessoas, request.data.get("professor_id"))
            if not professor:
                return Response(
                    {"res": "Não existe professor com o id informado"}, 
                    status=st.HTTP_400_BAD_REQUEST
                )
            alocacao.professor = professor
        else:
            alocacao.professor = None

        if request.data.get("data_inicio"):
            data_inicio = datetime.strptime(request.data.get("data_inicio"), "%Y-%m-%d").date()
            alocacao.data_inicio = data_inicio
        else:
            alocacao.data_inicio = None
            
        if request.data.get("data_fim"):
            data_fim = datetime.strptime(request.data.get("data_fim"), "%Y-%m-%d").date()
            alocacao.data_fim = data_fim
        else:
            alocacao.data_fim = None
        
        if request.data.get("status"):
            status = request.data.get("status") 
            alocacao.status = status
        else:
            alocacao.status = None
        
        if request.data.get("observacao"):
            observacao = request.data.get("observacao")
            alocacao.observacao = observacao
        else:
            alocacao.observacao = None
        
        if request.data.get("logradouro"):
            logradouro = request.data.get("logradouro")
            alocacao.logradouro = logradouro
        else:
            alocacao.logradouro = None

        if request.data.get("complemento"):
            complemento = request.data.get("complemento")
            alocacao.complemento = complemento
        else:
            alocacao.complemento = None

        if request.data.get("bairro"):
            bairro = request.data.get("bairro")
            alocacao.bairro = bairro
        else:
            alocacao.bairro = None

        if request.data.get("cidade_id"):
            cidade = self.get_object(Cidade, request.data.get("cidade_id"))
            if not cidade:
                return Response(
                    {"res": "Não existe cidade com o id informado"}, 
                    status=st.HTTP_400_BAD_REQUEST
                )
            alocacao.cidade = cidade
        else:
            alocacao.cidade = None
        
        if request.data.get("cep"):
            cep = request.data.get("cep")
            alocacao.cep = cep
        else:
            alocacao.cep = None

        print("aulas_sabado", request.data.get("aulas_sabado"))
        print("turnos", request.data.get("turnos"))
        if request.data.get("aulas_sabado") is not None:
            aulas_sabado = request.data.get("aulas_sabado")
            alocacao.aulas_sabado = aulas_sabado
        
        if request.data.get("turnos"):
            turnos = request.data.get("turnos")
            alocacao.turnos.set(turnos)

        alocacao.save()
        serializer = AlocacaoSerializer(alocacao)
        
        return Response(serializer.data, status=st.HTTP_200_OK)

    def delete(self, request, alocacao_id, *args, **kwargs):
        
        alocacao = self.get_object(Alocacao, alocacao_id)
        if not alocacao:
            return Response(
                {"res": "Não existe alocação com o id informado"}, 
                status=st.HTTP_400_BAD_REQUEST
            )
        alocacao.delete()
        return Response(
            {"res": "alocação deletada!"},
            status=st.HTTP_200_OK
        )
