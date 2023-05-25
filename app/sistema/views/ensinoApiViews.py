# todo/todo_api/views.py
from datetime import datetime
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status as str
from django.db import transaction
from django.db.models import Q, Prefetch
from ..models.cidade import Cidade
from ..models.ticket  import Ticket
from ..models.escola import Escola
from ..models.alocacao import Alocacao
from ..models.endereco import Endereco
from ..models.ensino import Ensino
from ..models.dpEvento import DpEvento
from ..services.anexoService import AnexoService
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
        first_dp_evento_prefetch = Prefetch('dpevento_set', queryset=DpEvento.objects.all(), to_attr='first_dp_evento')

        ensinos = Ensino.objects.prefetch_related(first_dp_evento_prefetch).select_related('escola', 'cidade')
        if observacao:
            ensinos = ensinos.filter(observacao__icontains=observacao)
        if data_inicio and not data_fim:
            data_inicio = datetime.strptime(data_inicio, '%Y-%m-%d')
            data_inicio = datetime.combine(data_inicio, datetime.min.time())
            ensinos = ensinos.filter(data_inicio__gte=data_inicio)
        if data_fim and not data_inicio:
            data_fim = datetime.strptime(data_fim, '%Y-%m-%d')
            data_fim = datetime.combine(data_fim, datetime.max.time())
            ensinos = ensinos.filter(data_fim__lte=data_fim)
        if data_inicio and data_fim:
            data_fim = datetime.strptime(data_fim, '%Y-%m-%d')
            data_fim = datetime.combine(data_fim, datetime.max.time())
            data_inicio = datetime.strptime(data_inicio, '%Y-%m-%d')
            data_inicio = datetime.combine(data_inicio, datetime.min.time())
            ensinos = ensinos.filter(Q(data_inicio__range=[data_inicio, data_fim]) | 
                                 Q(data_fim__range=[data_inicio, data_fim]))
        if escolas:
            ensinos = ensinos.filter(escola__id__in=escolas)
        if order_by:
            ensinos = ensinos.order_by(order_by)
        else:
            ensinos = ensinos.order_by("-data_inicio")
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
        etapa = request.data.get("etapa")
        bairro = request.data.get("bairro")
        cep = request.data.get("cep")
        complemento = request.data.get("complemento")
        status = request.data.get("status")
        tipo = request.data.get("tipo")
        numero_oficio = request.data.get("numero_oficio")
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
        with transaction.atomic():
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
                escola = escola,
                numero_oficio = numero_oficio,
                etapa = etapa
            )

            anexoService = AnexoService()
            anexoOficioDataUrl = request.data.get("oficio_data_url")
            anexoOficioNome = request.data.get("oficio_name")
            
            if anexoOficioDataUrl:
                oficioData = {
                    "dataUrl": anexoOficioDataUrl,
                    "nome": anexoOficioNome,
                    "model": "Ensino",
                    "id_model": ensino.id,
                }
                anexoOficio = anexoService.create_anexo(oficioData)
                extension =  anexoOficio.nome.split(".")[-1]
                anexoOficio.nome = f"oficio_{numero_oficio}.{extension}"
                anexoOficio.save()
                ensino.anexo_oficio = anexoOficio
                ensino.save()
            
            first_dp_evento_prefetch = Prefetch('dpevento_set', queryset=DpEvento.objects.all(), to_attr='first_dp_evento')
            ensino = Ensino.objects.prefetch_related(first_dp_evento_prefetch).select_related('escola', 'cidade', 'anexo_oficio').get(id=ensino.id)
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
        first_dp_evento_prefetch = Prefetch('dpevento_set', queryset=DpEvento.objects.all(), to_attr='first_dp_evento')
        ensino = Ensino.objects.prefetch_related(first_dp_evento_prefetch).select_related('escola', 'cidade').get(id=ensino_id)
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
        if request.data.get("etapa"):
            ensino.etapa = request.data.get("etapa")
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
        if request.data.get("numero_oficio"):
            ensino.numero_oficio = request.data.get("numero_oficio")

        if request.data.get("oficio_data_url"):
            anexoService = AnexoService()
            anexoOficioDataUrl = request.data.get("oficio_data_url")
            anexoOficioNome = request.data.get("oficio_name")
            oficioData = {
                "dataUrl": anexoOficioDataUrl,
                "nome": anexoOficioNome,
                "model": "Ensino",
                "id_model": ensino.id,
            }

            anexoOficio = anexoService.create_anexo(oficioData)
            extension =  anexoOficio.nome.split(".")[-1]
            anexoOficio.nome = f"oficio_{ensino.numero_oficio}.{extension}"
            anexoOficio.save()
            ensino.anexo_oficio = anexoOficio
            ensino.save()
        else: ensino.save()
        first_dp_evento_prefetch = Prefetch('dpevento_set', queryset=DpEvento.objects.all(), to_attr='first_dp_evento')
        ensino = Ensino.objects.prefetch_related(first_dp_evento_prefetch).select_related('escola', 'cidade').get(id=ensino.id)
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
                demandas = Ticket.objects.filter(alocacao=alocacao)
                for demanda in demandas:
                    demanda.delete()
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