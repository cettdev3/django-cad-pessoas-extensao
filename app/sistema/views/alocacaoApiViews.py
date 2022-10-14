# todo/todo_api/views.py
from datetime import datetime
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status as st
from rest_framework import permissions

from ..models.endereco import Endereco
from ..models.alocacao import Alocacao
from ..models.pessoa import Pessoas
from ..models.evento import Evento
from ..models.curso import Curso
from ..serializers.alocacaoSerializer import AlocacaoSerializer
from ..serializers.pessoaSerializer import PessoaSerializer
from ..serializers.eventoSerializer import EventoSerializer

class AlocacaoApiView(APIView):
    permission_classes = [permissions.AllowAny]
    def get_object(self, fn, object_id):
        try:
            return fn.objects.get(id=object_id)
        except fn.DoesNotExist:
            return None

    def get(self, request, *args, **kwargs):
        alocacoes = Alocacao.objects.all()
        serializer = AlocacaoSerializer(alocacoes, many=True)
        return Response(serializer.data, status=st.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        evento = None
        professor = None
        curso = None
        
        print("dados para requisição de alocações",len(request.data),request.data)
        if isinstance(request.data, list):
            alocacoesCriadas = []
            for alocacaoData in request.data:
                evento = None
                professor = None
                curso = None
                print("alocação data", alocacaoData)
                if alocacaoData["curso_id"]:
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
                alocacao = Alocacao.objects.create(
                    data_inicio = data_inicio,
                    data_fim = data_fim,
                    observacao = observacao,
                    status = status,
                    evento = evento,
                    professor = professor,
                    curso = curso,
                )

                alocacaoSerializer = AlocacaoSerializer(alocacao)
                alocacoesCriadas.append(alocacaoSerializer.data)
            return Response(alocacoesCriadas, status=st.HTTP_201_CREATED)
        else:
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
            if request.data.get("data_inicio"):
                print
                data_inicio = datetime.strptime(request.data.get("data_inicio"), "%Y-%m-%d").date()
            if request.data.get("data_fim"):
                data_fim = datetime.strptime(request.data.get("data_fim"), "%Y-%m-%d").date()
            status = request.data.get("status") 
            observacao = request.data.get("observacao") 

            alocacao = Alocacao.objects.create(
                data_inicio = data_inicio,
                data_fim = data_fim,
                observacao = observacao,
                status = status,
                evento = evento,
                professor = professor,
                curso = curso,
            )

            alocacaoSerializer = AlocacaoSerializer(alocacao)
            return Response(alocacaoSerializer.data, status=st.HTTP_201_CREATED)

class AlocacaoDetailApiView(APIView):
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