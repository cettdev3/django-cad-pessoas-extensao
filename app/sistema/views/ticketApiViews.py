from datetime import datetime
from rest_framework.views import APIView
from django.db.models import Q
from rest_framework.response import Response
from rest_framework import status as st
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from ..models.ticket import Ticket
from ..models.alocacao import Alocacao
from ..models.membroExecucao import MembroExecucao
from ..models.cidade import Cidade
from ..serializers.ticketSerializers.ticketSerializer import TicketSerializer 
from rest_framework_simplejwt.authentication import JWTAuthentication

class TicketApiView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication, JWTAuthentication]
    
    def get_object(self, fn, object_id):
        try:
            return fn.objects.get(id=object_id)
        except fn.DoesNotExist:
            return None

    def get(self, request, *args, **kwargs):
        ticket = Ticket.objects.select_related("membro_execucao", "alocacao").all()
        serializer = TicketSerializer(ticket, many=True)
        return Response(serializer.data, status=st.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        membro_execucao = None
        alocacao = None
        model = request.data.get("model")
        if request.data.get("membro_execucao_id"):
            membro_execucao = self.get_object(MembroExecucao, request.data.get("membro_execucao_id"))
            if not membro_execucao and model == "membro_execucao":
                return Response(
                    {"res": "Não existe membro da equipe de execução com o id informado"},
                    status=st.HTTP_400_BAD_REQUEST,
                )

        if request.data.get("alocacao_id"):
            alocacao = self.get_object(Alocacao, request.data.get("alocacao_id"))
            if not alocacao and model == "alocacao":
                return Response(
                    {"res": "Não existe alocação com o id informado"},
                    status=st.HTTP_400_BAD_REQUEST,
                )
        
        print("model: ", model)
        print("membro_execucao: ", membro_execucao)
        print("alocacao: ", alocacao)
            
        cidade = None
        if request.data.get("cidade_id"):
            cidade = self.get_object(Cidade, request.data.get("cidade_id"))
            if not cidade:
                return Response(
                    {"res": "Não existe cidade com o id informado"},
                    status=st.HTTP_400_BAD_REQUEST,
                )

        id_protocolo = request.data.get("id_protocolo")
        dataInicio = request.data.get("data_inicio") if request.data.get("data_inicio") else None
        dataFim = request.data.get("data_fim") if request.data.get("data_fim") else None
        nsa_data_inicio = request.data.get("nsa_data_inicio")
        nsa_data_fim = request.data.get("nsa_data_fim")
        if nsa_data_inicio == "on":
            dataInicio = None
        if nsa_data_fim == "on":
            dataFim = None

        ticketData = {
            "tipo": request.data.get("tipo"),
            "status": Ticket().STATUS_CRIADO if len(id_protocolo) > 0 else Ticket().STATUS_CRIACAO_PENDENTE,
            "id_protocolo": id_protocolo, 
            "membro_execucao":  membro_execucao,
            "alocacao": alocacao,
            "model": model,
            "meta": request.data.get("meta"),
            "data_inicio": dataInicio,
            "data_fim": dataFim,
            "nao_se_aplica_data_inicio": request.data.get("nsa_data_inicio") == "on",
            "nao_se_aplica_data_fim": request.data.get("nsa_data_fim") == "on",
            "bairro": request.data.get("bairro") ,
            "logradouro": request.data.get("logradouro"),
            "cep": request.data.get("cep"),
            "complemento": request.data.get("complemento"),
            "cidade":   cidade,
            "observacao": request.data.get("observacao"),
        }
    
        ticketData = Ticket.objects.create(**ticketData)
        ticketSerializer = TicketSerializer(ticketData)
        return Response(ticketSerializer.data, status=st.HTTP_200_OK)

class TicketDetailApiView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def get_object(self, fn, object_id):
        try:
            return fn.objects.get(id=object_id)
        except fn.DoesNotExist:
            return None
            
    def get(self, request, ticket_id, *args, **kwargs):

        ticket = self.get_object(Ticket, ticket_id)
        if not ticket:
            return Response(
                {"res": "Não existe ticket com o id informado"},
                status=st.HTTP_400_BAD_REQUEST
            )

        serializer = TicketSerializer(ticket)
        return Response(serializer.data, status=st.HTTP_200_OK)

    def put(self, request, ticket_id, *args, **kwargs):
        print("dentro do put")
        print(request.data)
        ticket = self.get_object(Ticket, ticket_id)
        if not ticket:
                return Response(
                    {"res": "Não existe ticket com o id informado"}, 
                    status=st.HTTP_400_BAD_REQUEST
                )
        if request.data.get("tipo"):
            ticket.tipo = request.data.get("tipo") 
        if request.data.get("id_protocolo"):
            id_protocolo = request.data.get("id_protocolo")
            if len(id_protocolo) > 0:
                ticket.status = Ticket().STATUS_CRIADO
            ticket.id_protocolo = request.data.get("id_protocolo")
        if request.data.get("meta"):
            ticket.meta = request.data.get("meta")
        if request.data.get("data_inicio"):
            ticket.data_inicio = request.data.get("data_inicio")
        if request.data.get("data_fim"):
            ticket.data_fim = request.data.get("data_fim")
        if request.data.get("bairro"):
            ticket.bairro = request.data.get("bairro")
        if request.data.get("logradouro"):
            ticket.logradouro = request.data.get("logradouro")
        if request.data.get("cep"):
            ticket.cep = request.data.get("cep")
        if request.data.get("complemento"):
            ticket.complemento = request.data.get("complemento")
        if request.data.get("cidade_id"):
            cidade = self.get_object(Cidade, request.data.get("cidade_id"))
            if not cidade:
                return Response(
                    {"res": "Não existe cidade com o id informado"},
                    status=st.HTTP_400_BAD_REQUEST,
                )
            ticket.cidade = cidade
        if request.data.get("observacao"):
            ticket.observacao = request.data.get("observacao")


        nsaDataInicio = request.data.get("nsa_data_inicio")
        nsaDataFim = request.data.get("nsa_data_fim")

        saveDataInicio = nsaDataInicio == "on"
        ticket.nao_se_aplica_data_inicio = saveDataInicio
        if saveDataInicio:
            ticket.data_inicio = None
        
        saveDataFim = nsaDataFim == "on"
        ticket.nao_se_aplica_data_fim = saveDataFim
        if saveDataFim:
            ticket.data_fim = None
        
        ticket.save()
        serializer = TicketSerializer(ticket)
       
        print(serializer.data)
        return Response(serializer.data, status=st.HTTP_200_OK)

    def delete(self, request, ticket_id, *args, **kwargs):
        
        ticket = self.get_object(Ticket, ticket_id)
        if not ticket:
            return Response(
                {"res": "Não existe ticket com o id informado"}, 
                status=st.HTTP_400_BAD_REQUEST
            )
        ticket.delete()
        return Response(
            {"res": "ticket deletado!"},
            status=st.HTTP_200_OK
        )