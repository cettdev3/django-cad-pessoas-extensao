# todo/todo_api/views.py
from datetime import datetime
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status as str
from rest_framework import permissions
from django.db import transaction
from ..models.cidade import Cidade
from ..models.escola import Escola
from ..models.alocacao import Alocacao
from ..models.endereco import Endereco
from ..models.ensino import Ensino
from ..serializers.ensinoSerializer import EnsinoSerializer
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

class EnsinoApiView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def get_object(self, fn, object_id):
        try:
            return fn.objects.get(id=object_id)
        except fn.DoesNotExist:
            return None

    def get(self, request, *args, **kwargs):
        eventos = Ensino.objects.all()
        serializer = EnsinoSerializer(eventos, many=True)
        return Response(serializer.data, status=str.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        data_inicio = None
        data_fim = None
        if request.data.get("data_inicio"):
            data_inicio = datetime.strptime(request.data.get("data_inicio"), '%Y-%m-%dT%H:%M')
        if request.data.get("data_fim"):
            data_fim = datetime.strptime(request.data.get("data_fim"), '%Y-%m-%dT%H:%M')
        observacao = request.data.get("observacao")
        logradouro = request.data.get("logradouro")
        bairro = request.data.get("bairro")
        cep = request.data.get("cep")
        complemento = request.data.get("complemento")
        status = request.data.get("status")
        tipo = request.data.get("tipo")
        endereco = None
        escola = None
        cidade = None

        if request.data.get("endereco_id"):
            endereco = self.get_object(Endereco, request.data.get("endereco_id"))

            if not endereco:
                return Response(
                    {"res": "Não existe endereco com o id informado"},
                    status=str.HTTP_400_BAD_REQUEST
                )
        
        if request.data.get("escola_id"):
            escola = self.get_object(Escola, request.data.get("escola_id"))

            if not escola:
                return Response(
                    {"res": "Não existe escola com o id informado"},
                    status=str.HTTP_400_BAD_REQUEST
                )
        
        if request.data.get("cidade_id"):
            cidade = self.get_object(Cidade, request.data.get("cidade_id"))

            if not cidade:
                return Response(
                    {"res": "Não existe cidade com o id informado"},
                    status=str.HTTP_400_BAD_REQUEST
                )

        evento = Ensino.objects.create(
            data_inicio = data_inicio,
            data_fim = data_fim,
            observacao = observacao,
            status = status,
            tipo = tipo,
            logradouro = logradouro,
            complemento = complemento,
            bairro = bairro,
            cidade = cidade,
            cep = cep,
            escola = escola
        )

        eventoSerializer = EnsinoSerializer(evento)
        return Response(eventoSerializer.data, status=str.HTTP_201_CREATED)

class EnsinoDetailApiView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    
    def get_object(self, fn, object_id):
        try:
            return fn.objects.get(id=object_id)
        except fn.DoesNotExist:
            return None
            
    def get(self, request, evento_id, *args, **kwargs):

        evento = self.get_object(Ensino, evento_id)
        if not evento:
            return Response(
                {"res": "Não existe evento com o id informado"},
                status=str.HTTP_400_BAD_REQUEST
            )

        serializer = EnsinoSerializer(evento)
        return Response(serializer.data, status=str.HTTP_200_OK)

    def put(self, request, evento_id, *args, **kwargs):

        evento = self.get_object(Ensino, evento_id)
        if not evento:
            return Response(
                {"res": "Não existe evento com o id informado"}, 
                status=str.HTTP_400_BAD_REQUEST
            )

        if request.data.get("data_inicio"):
            evento.data_inicio = datetime.strptime(request.data.get("data_inicio"), '%Y-%m-%dT%H:%M')
        if request.data.get("data_fim"):
            evento.data_fim = datetime.strptime(request.data.get("data_fim"), '%Y-%m-%dT%H:%M')
        if request.data.get("observacao"):
            evento.observacao = request.data.get("observacao")
        if request.data.get("status"):
            evento.status = request.data.get("status")
        if request.data.get("tipo"):
            evento.tipo = request.data.get("tipo")
        if request.data.get("logradouro"):
            evento.logradouro = request.data.get("logradouro")
        if request.data.get("complemento"):
            evento.complemento = request.data.get("complemento")
        if request.data.get("bairro"):
            evento.bairro = request.data.get("bairro")
        if request.data.get("cidade_id"):
            cidade = self.get_object(Cidade, request.data.get("cidade_id"))
            if not cidade:
                return Response(
                    {"res": "Não existe evento com o id informado"}, 
                    status=str.HTTP_400_BAD_REQUEST
                )
            evento.cidade = cidade
        if request.data.get("escola_id"):
            escola = self.get_object(Escola, request.data.get("escola_id"))
            if not escola:
                return Response(
                    {"res": "Não existe escola com o id informado"}, 
                    status=str.HTTP_400_BAD_REQUEST
                )
            evento.escola = escola
        if request.data.get("cep"):
            evento.cep = request.data.get("cep")

        evento.save()
        serializer = EnsinoSerializer(evento)
        
        return Response(serializer.data, status=str.HTTP_200_OK)

    def delete(self, request, ensino_id, *args, **kwargs):
        
        ensino = self.get_object(Ensino, ensino_id)
        if not ensino:
            return Response(
                {"res": "Não existe ação de ensino com o id informado"}, 
                status=str.HTTP_400_BAD_REQUEST
            )
        with transaction.atomic():
            # try:
            alocacoes = Alocacao.objects.filter(evento__id=ensino.id)
            for alocacao in alocacoes:
                alocacao.delete()
            ensino.delete()
            # except Exception as e:
            #     return Response(
            #         {"res": "Não foi possível deletar a ação de ensino"}, 
            #         status=str.HTTP_400_BAD_REQUEST
            #     )

        return Response(
            {"res": "ensino deletada!"},
            status=str.HTTP_200_OK
        )