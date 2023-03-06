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
        order_by = request.GET.get('order_by') if request.GET.get('order_by') != "None" else None
        observacao = request.GET.get('observacao') if request.GET.get('observacao') != "None" else None
        data_inicio = request.GET.get('data_inicio') if request.GET.get('data_inicio') != "None" else None
        data_fim = request.GET.get('data_fim') if request.GET.get('data_fim') != "None" else None
        escolas = request.GET.getlist('escolas') if request.GET.getlist('escolas') != "None" else None

        ensinos = Ensino.objects
        if observacao:
            ensinos = ensinos.filter(observacao__icontains=observacao)
        if data_inicio:
            data_inicio = datetime.strptime(data_inicio, '%Y-%m-%d')
            data_inicio = datetime.combine(data_inicio, datetime.min.time())
            ensinos = ensinos.filter(data_inicio__gte=data_inicio)
        if data_fim:
            data_fim = datetime.strptime(data_fim, '%Y-%m-%d')
            data_fim = datetime.combine(data_fim, datetime.max.time())
            ensinos = ensinos.filter(data_fim__lte=data_fim)
        if escolas:
            ensinos = ensinos.filter(escola__id__in=escolas)
        if order_by:
            ensinos = ensinos.order_by(order_by)
        else:
            ensinos = ensinos.order_by("data_inicio")
        ensinos = ensinos.all()
        serializer = EnsinoSerializer(ensinos, many=True)
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

        ensino = Ensino.objects.create(
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

        ensinoSerializer = EnsinoSerializer(ensino)
        return Response(ensinoSerializer.data, status=str.HTTP_201_CREATED)

class EnsinoDetailApiView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    
    def get_object(self, fn, object_id):
        try:
            return fn.objects.get(id=object_id)
        except fn.DoesNotExist:
            return None
            
    def get(self, request, ensino_id, *args, **kwargs):

        ensino = self.get_object(Ensino, ensino_id)
        if not ensino:
            return Response(
                {"res": "Não existe ensino com o id informado"},
                status=str.HTTP_400_BAD_REQUEST
            )

        serializer = EnsinoSerializer(ensino)
        return Response(serializer.data, status=str.HTTP_200_OK)

    def put(self, request, ensino_id, *args, **kwargs):

        ensino = self.get_object(Ensino, ensino_id)
        if not ensino:
            return Response(
                {"res": "Não existe ensino com o id informado"}, 
                status=str.HTTP_400_BAD_REQUEST
            )

        if request.data.get("data_inicio"):
            ensino.data_inicio = datetime.strptime(request.data.get("data_inicio"), '%Y-%m-%dT%H:%M')
        if request.data.get("data_fim"):
            ensino.data_fim = datetime.strptime(request.data.get("data_fim"), '%Y-%m-%dT%H:%M')
        if request.data.get("observacao"):
            ensino.observacao = request.data.get("observacao")
        if request.data.get("status"):
            ensino.status = request.data.get("status")
        if request.data.get("tipo"):
            ensino.tipo = request.data.get("tipo")
        if request.data.get("logradouro"):
            ensino.logradouro = request.data.get("logradouro")
        if request.data.get("complemento"):
            ensino.complemento = request.data.get("complemento")
        if request.data.get("bairro"):
            ensino.bairro = request.data.get("bairro")
        if request.data.get("cidade_id"):
            cidade = self.get_object(Cidade, request.data.get("cidade_id"))
            if not cidade:
                return Response(
                    {"res": "Não existe ensino com o id informado"}, 
                    status=str.HTTP_400_BAD_REQUEST
                )
            ensino.cidade = cidade
        if request.data.get("escola_id"):
            escola = self.get_object(Escola, request.data.get("escola_id"))
            if not escola:
                return Response(
                    {"res": "Não existe escola com o id informado"}, 
                    status=str.HTTP_400_BAD_REQUEST
                )
            ensino.escola = escola
        if request.data.get("cep"):
            ensino.cep = request.data.get("cep")

        ensino.save()
        serializer = EnsinoSerializer(ensino)
        
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
            alocacoes = Alocacao.objects.filter(acaoEnsino__id=ensino.id)
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