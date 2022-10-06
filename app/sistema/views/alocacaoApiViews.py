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
        if request.data.get("evento_id"):
            evento = self.get_object(Evento, request.data.get("evento_id"))
            if not evento:
                return Response(
                    {"res": "Não existe evento com o id informado"}, 
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
            data_inicio = datetime.strptime(request.data.get("data_inicio"), "%d-%m-%Y").date()
        if request.data.get("data_fim"):
            data_fim = datetime.strptime(request.data.get("data_fim"), "%d-%m-%Y").date()
        status = request.data.get("status") 
        observacao = request.data.get("observacao") 

        alocacao = Alocacao.objects.create(
            data_inicio = data_inicio,
            data_fim = data_fim,
            observacao = observacao,
            status = status,
            evento = evento,
            professor = professor
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
            data_inicio = datetime.strptime(request.data.get("data_inicio"), "%d-%m-%Y").date()
            alocacao.data_inicio = data_inicio
        else:
            alocacao.data_inicio = None
            
        if request.data.get("data_fim"):
            data_fim = datetime.strptime(request.data.get("data_fim"), "%d-%m-%Y").date()
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