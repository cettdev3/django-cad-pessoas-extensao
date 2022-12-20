from datetime import datetime
from rest_framework.views import APIView
from django.db.models import Q
from rest_framework.response import Response
from rest_framework import status as st
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from ..models.ticket import Ticket
from ..models.acao import Acao
from ..models.membroExecucao import MembroExecucao
from ..serializers.ticketSerializer import TicketSerializer 
from sistema.services.camunda import CamundaAPI 
import json
import time
class TicketApiView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    
    def get_object(self, fn, object_id):
        try:
            return fn.objects.get(id=object_id)
        except fn.DoesNotExist:
            return None

    def get(self, request, *args, **kwargs):
        ticket = Ticket.objects.all()
        serializer = TicketSerializer(ticket, many=True)
        return Response(serializer.data, status=st.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        membro_execucao = None
        if request.data.get("membro_execucao_id"):
            membro_execucao = self.get_object(MembroExecucao, request.data.get("membro_execucao_id"))
            if not membro_execucao:
                return Response(
                    {"res": "Não existe membro da equipe de execução com o id informado"},
                    status=st.HTTP_400_BAD_REQUEST,
                )

            ticket = Ticket.objects.filter(membro_execucao=membro_execucao, status="CREATED")
            if ticket.exists():
                message = "Já existe um ticket com status CREATED para o membro da equipe de execução informado. "
                message += "Ticket id: " + str(ticket[0].id_protocolo) + " Ticket tipo: " + ticket[0].tipo
                return Response(
                    {"res": message},
                    status=st.HTTP_400_BAD_REQUEST,
                )


        ticketData = {
            "tipo": request.data.get("tipo"),
            "status": "CREATED",
            "id_protocolo": request.data.get("id_protocolo"),
            "membro_execucao": membro_execucao,
            "meta": request.data.get("meta"),
        }
    
        ticketData = Ticket.objects.create(**ticketData)

        acao = membro_execucao.acao
        membersWithoutTickets = MembroExecucao.objects.filter( Q(acao__id=acao.id, ticket__isnull=True)).all()

        if len(membersWithoutTickets) == 0 and acao.status == Acao.STATUS_WAITING_TICKET:

            membersWithTickets = MembroExecucao.objects.filter( Q(acao__id=acao.id, ticket__isnull=False)).all()
            tickets = []
            for member in membersWithTickets:
                tickets.append({
                    "id_protocolo": member.ticket.id_protocolo, 
                    "tipo": member.ticket.tipo, 
                    "status": member.ticket.status,
                    "membro_execucao": member.pessoa.id,
                    "member_nome": member.pessoa.nome,
                    "member_cpf": member.pessoa.cpf,
                })

            dados = {
                "variables": {
                    "tickets": {"value": json.dumps(tickets), 
                    "type": "Json"},
                },
                "withVariablesInReturn": True
            }

            camundaApi = CamundaAPI()
            tasks = camundaApi.getTasks(acao.process_instance)
            tasksFromInstance = json.loads(tasks.content)
            for i,task in enumerate(tasksFromInstance):
                completedTask = camundaApi.completeTask(task["id"], variables=dados)
            
            acao.status = Acao.STATUS_WAITING_RETURN
            acao.save()

        acaoSerializer= TicketSerializer(ticketData)
        return Response(acaoSerializer.data, status=st.HTTP_200_OK)

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
        ticket = self.get_object(Ticket, ticket_id)
        if not ticket:
                return Response(
                    {"res": "Não existe ticket com o id informado"}, 
                    status=st.HTTP_400_BAD_REQUEST
                )

        membro_execucao = None
        if request.data.get("membro_execucao_id"):
            membro_execucao = self.get_object(MembroExecucao, request.data.get("membro_execucao_id"))
            if not membro_execucao:
                return Response(
                    {"res": "Não existe membro da equipe de execução com o id informado"}, 
                    status=st.HTTP_400_BAD_REQUEST
                )
            ticket.membro_execucao = membro_execucao

        if request.data.get("tipo"):
            ticket.tipo = request.data.get("tipo") 
        if request.data.get("status"):
            ticket.status = request.data.get("status")
        if request.data.get("id_protocolo"):
            ticket.id_protocolo = request.data.get("id_protocolo")
        if request.data.get("meta"):
            ticket.meta = request.data.get("meta")
        
        ticket.save()
        serializer = TicketSerializer(ticket)
        
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