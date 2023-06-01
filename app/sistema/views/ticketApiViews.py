from datetime import datetime
from rest_framework.views import APIView
from django.db.models import Q, Case, When, Value, CharField
from rest_framework.response import Response
from rest_framework import status as st, viewsets
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from ..models.ticket import Ticket
from ..models.alocacao import Alocacao
from ..models.escola import Escola
from ..models.departamento import Departamento
from ..models.pessoa import Pessoas
from ..models.atividade import Atividade
from ..models.membroExecucao import MembroExecucao
from ..models.cidade import Cidade
from ..serializers.ticketSerializers.ticketSerializer import TicketSerializer 
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.decorators import action
class TicketApiView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication, JWTAuthentication]
    
    def get_object(self, fn, object_id):
        try:
            return fn.objects.get(id=object_id)
        except fn.DoesNotExist:
            return None

    def get(self, request, *args, **kwargs):
        status = request.GET.get("status")
        favorecido = request.GET.get("favorecido")
        escola = request.GET.get("escola")
        order_by = request.GET.get("order_by")
        id_protocolo = request.GET.get("id_protocolo")
        print("dentro da rota de tickets: ", id_protocolo)
        tickets = Ticket.objects.select_related("membro_execucao", "alocacao", "pessoa", "atividade")
        if favorecido:
            tickets = tickets.filter(Q(membro_execucao__pessoa__nome__icontains=favorecido) | Q(alocacao__professor__nome__icontains=favorecido) | Q(pessoa__nome__icontains=favorecido))
        if escola:
            tickets = tickets.filter(
                Q(membro_execucao__evento__escolas__nome__icontains=escola) | 
                Q(alocacao__acaoEnsino__escola__nome__icontains=escola) | 
                Q(escola__nome__icontains=escola)
            )
        if id_protocolo:
            tickets = tickets.filter(id_protocolo=id_protocolo)
        
        if order_by and order_by == "favorecido":
            tickets = tickets.annotate(
                pessoa_name=Case(
                    When(alocacao__isnull=False, then='alocacao__professor__nome'),
                    When(membro_execucao__isnull=False, then='membro_execucao__pessoa__nome'),
                    When(pessoa__isnull=False, then='pessoa__nome'),
                    default=Value(''),
                    output_field=CharField(),
                ),
            ).order_by(order_by)

        tickets = tickets.all()
        serializer = TicketSerializer(tickets, many=True)
        serialized_data = serializer.data

        if status:
            serialized_data = [item for item in serializer.data if item['status_calculado'] == status]
        if order_by and order_by == "status":
            serialized_data = sorted(serialized_data, key=lambda k: k['status_calculado'])
        
        return Response(serialized_data, status=st.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        membro_execucao = None
        alocacao = None
        pessoa = None
        atividade = None
        model = request.data.get("model")
        escola = None
        cidade = None
        beneficiario = None
        departamento = None

        if request.data.get("membro_execucao_id"):
            membro_execucao = self.get_object(MembroExecucao, request.data.get("membro_execucao_id"))
            if not membro_execucao and model == "membro_execucao":
                return Response(
                    {"res": "Não existe membro da equipe de execução com o id informado"},
                    status=st.HTTP_400_BAD_REQUEST,
                )
            beneficiario = membro_execucao.pessoa

        if request.data.get("alocacao_id"):
            alocacao = self.get_object(Alocacao, request.data.get("alocacao_id"))
            if not alocacao and model == "alocacao":
                return Response(
                    {"res": "Não existe alocação com o id informado"},
                    status=st.HTTP_400_BAD_REQUEST,
                )
            beneficiario = alocacao.professor
            
        if request.data.get("pessoa_id"):
            pessoa = self.get_object(Pessoas, request.data.get("pessoa_id"))
            if not pessoa:
                return Response(
                    {"res": "Não existe pessoa com o id informado"},
                    status=st.HTTP_400_BAD_REQUEST,
                )
        
        if request.data.get("atividade_id"):
            atividade = self.get_object(Atividade, request.data.get("atividade_id"))
            if not atividade:
                return Response(
                    {"res": "Não existe atividade com o id informado"},
                    status=st.HTTP_400_BAD_REQUEST,
                )

        if request.data.get("escola_id"):
            escola = self.get_object(Escola, request.data.get("escola_id"))
            if not escola:
                return Response(
                    {"res": "Não existe escola com o id informado"},
                    status=st.HTTP_400_BAD_REQUEST,
                )
            
        if request.data.get("cidade_id"):
            cidade = self.get_object(Cidade, request.data.get("cidade_id"))
            if not cidade:
                return Response(
                    {"res": "Não existe cidade com o id informado"},
                    status=st.HTTP_400_BAD_REQUEST,
                )
            
        if request.data.get("beneficiario_id"):
            beneficiario = self.get_object(Pessoas, request.data.get("beneficiario_id"))
            if not beneficiario:
                return Response(
                    {"res": "Não existe beneficiario com o id informado"},
                    status=st.HTTP_400_BAD_REQUEST,
                )
        
        if request.data.get("departamento_id"):
            departamento = self.get_object(Departamento, request.data.get("departamento_id"))
            if not departamento:
                return Response(
                    {"res": "Não existe departamento com o id informado"},
                    status=st.HTTP_400_BAD_REQUEST,
                )
            
        dataInicio = None
        dataFim = None

        if request.data.get("data_inicio") and request.data.get("data_inicio") != "":
            if request.data.get("nao_se_aplica_data_inicio") not in ["on", True]:
                dataInicio = request.data.get("data_inicio")
        
        if request.data.get("data_fim") and request.data.get("data_fim") != "":
            if request.data.get("nao_se_aplica_data_fim") not in ["on", True]:
                dataFim = request.data.get("data_fim")
        
        nao_se_aplica_data_inicio = False
        if request.data.get("nao_se_aplica_data_inicio") in ["on","off", True, False]:
            nsaDataInicio = request.data.get("nao_se_aplica_data_inicio")
            if nsaDataInicio == "on":
                nsaDataInicio = True
            elif nsaDataInicio == "off":
                nsaDataInicio = False
            nao_se_aplica_data_inicio = nsaDataInicio

        nao_se_aplica_data_fim = False
        if request.data.get("nao_se_aplica_data_fim") in ["on","off", True, False]:
            nsaDataFim = request.data.get("nao_se_aplica_data_fim")
            if nsaDataFim == "on":
                nsaDataFim = True
            elif nsaDataFim == "off":
                nsaDataFim = False
            nao_se_aplica_data_fim = nsaDataFim

        id_protocolo = request.data.get("id_protocolo", "")

        status = request.data.get("status") if request.data.get("status") else Ticket().STATUS_CRIACAO_PENDENTE
        if len(id_protocolo) > 0:
            ticketFromIdProtocolo = Ticket.objects.filter(id_protocolo=id_protocolo).first()
            if ticketFromIdProtocolo:
                evento = None
                mensagem = "Já existe um ticket com o protocolo informado: "+id_protocolo+". O id do ticket no Maestro é: "+str(ticketFromIdProtocolo.id)+"; "
                membroExecucaoTicket = ticketFromIdProtocolo.membro_execucao
                if membroExecucaoTicket:
                    evento = membroExecucaoTicket.evento
                    mensagem += "Membro da equipe de execução, "+ membroExecucaoTicket.pessoa.nome+";"
                alocacaoTicket = ticketFromIdProtocolo.alocacao
                if alocacaoTicket:
                    evento = alocacaoTicket.acaoEnsino
                    mensagem += "Alocação do professor, "+ alocacaoTicket.professor.nome +", no curso de: "+alocacaoTicket.curso.nome +";"
                atividadeTicket = ticketFromIdProtocolo.atividade
                if atividadeTicket:
                    evento = atividadeTicket.evento
                    mensagem += "Atividade, "+ atividadeTicket.tipoAtividade.nome +";"
                if evento:
                    mensagem += "evento: " + evento.tipo + " de " + evento.data_inicio_formatada + " a " + evento.data_fim_formatada
                return Response(
                    {"res": mensagem, "ticket_id": ticketFromIdProtocolo.id},
                    status=st.HTTP_400_BAD_REQUEST,
                )

            if request.data.get("status") in [Ticket().STATUS_CRIADO, Ticket().STATUS_PRESTACAO_CONTAS_PENDENTE, Ticket().STATUS_PRESTACAO_CONTAS_CRIADA, Ticket().STATUS_CANCELADO]:
                status = request.data.get("status")
            else:
                status = Ticket().STATUS_CRIADO
        elif request.data.get("status") in [Ticket().STATUS_CRIADO, Ticket().STATUS_CRIACAO_PENDENTE]:
            status = request.data.get("status")
        
        valor_orcado = None
        if request.data.get("valor_orcado") and request.data.get("valor_orcado") != "":
            valor_orcado = request.data.get("valor_orcado")

        valor_executado = None
        if request.data.get("valor_executado") and request.data.get("valor_executado") != "":
            valor_executado = request.data.get("valor_executado")

        if request.data.get("tipo"):
            tipo = request.data.get("tipo")
            if tipo not in Ticket().TIPOS:
                message = f"Tipo de inválido. Tipo fornecido: {tipo}. Tipos válidos: {Ticket().TIPOS}"
                return Response(
                    {"res": message},
                    status=st.HTTP_400_BAD_REQUEST,
                )

        ticketData = {
            "tipo": request.data.get("tipo"),
            "status": status,
            "id_protocolo": id_protocolo, 
            "membro_execucao":  membro_execucao,
            "alocacao": alocacao,
            "pessoa": pessoa,
            "atividade": atividade,
            "escola": escola,
            "model": model,
            "meta": request.data.get("meta"),
            "data_inicio": dataInicio,
            "data_fim": dataFim,
            "nao_se_aplica_data_inicio": nao_se_aplica_data_inicio,
            "nao_se_aplica_data_fim": nao_se_aplica_data_fim,
            "bairro": request.data.get("bairro") ,
            "logradouro": request.data.get("logradouro"),
            "cep": request.data.get("cep"),
            "complemento": request.data.get("complemento"),
            "cidade":   cidade,
            "observacao": request.data.get("observacao"),
            "valor_orcado": valor_orcado,
            "valor_executado": valor_executado,
            "beneficiario": beneficiario,
            "rubrica": request.data.get("rubrica"),
            "departamento": departamento,
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
        if  request.data.get("data_inicio"):
            if request.data.get("nao_se_aplica_data_inicio") not in ["on", True] and len(request.data.get("data_inicio")) > 0 :
                ticket.data_inicio = request.data.get("data_inicio")
        if request.data.get("data_fim"):
            if  request.data.get("nao_se_aplica_data_fim") not in ["on", True] and len(request.data.get("data_fim")) > 0:
                ticket.data_fim = request.data.get("data_fim")
        if request.data.get("valor_orcado") and request.data.get("valor_orcado") != "":
            ticket.valor_orcado = request.data.get("valor_orcado")
        if request.data.get("valor_executado") and request.data.get("valor_executado") != "":
            ticket.valor_executado = request.data.get("valor_executado")
        if request.data.get("bairro"):
            ticket.bairro = request.data.get("bairro")
        if request.data.get("logradouro"):
            ticket.logradouro = request.data.get("logradouro")
        if request.data.get("cep"):
            ticket.cep = request.data.get("cep")
        if request.data.get("complemento"):
            ticket.complemento = request.data.get("complemento")
        if request.data.get("rubrica"):
            ticket.rubrica = request.data.get("rubrica")
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
        if request.data.get("status"):
            if len(ticket.id_protocolo) > 0 and request.data.get("status") != Ticket().STATUS_CRIACAO_PENDENTE and request.data.get("status") != Ticket().STATUS_ATRASADO_PARA_CRIACAO:
                ticket.status = request.data.get("status")
        if request.data.get("pessoa_id"):
            pessoa = self.get_object(Pessoas, request.data.get("pessoa_id"))
            if not pessoa:
                return Response(
                    {"res": "Não existe pessoa com o id informado"},
                    status=st.HTTP_400_BAD_REQUEST,
                )
            ticket.pessoa = pessoa
        
        if request.data.get("atividade_id"):
            atividate_id = request.data.get("atividade_id") if type(request.data.get("atividade_id")) == int else int(request.data.get("atividade_id"))

            if atividate_id > 0:
                atividade = self.get_object(Atividade, request.data.get("atividade_id"))
                if not atividade:
                    return Response(
                        {"res": "Não existe atividade com o id informado"},
                        status=st.HTTP_400_BAD_REQUEST,
                    )
            else: 
                atividade = None
            ticket.atividade = atividade

        if request.data.get("escola_id"):
            escola = self.get_object(Escola, request.data.get("escola_id"))
            if not escola:
                return Response(
                    {"res": "Não existe escola com o id informado"},
                    status=st.HTTP_400_BAD_REQUEST,
                )
            ticket.escola = escola
        
        if request.data.get("departamento_id"):
            departamento = self.get_object(Departamento, request.data.get("departamento_id"))
            if not departamento:
                return Response(
                    {"res": "Não existe departamento com o id informado"},
                    status=st.HTTP_400_BAD_REQUEST,
                )
            ticket.departamento = departamento

        if request.data.get("beneficiario_id") or request.data.get("membro_execucao_id"):
            beneficiario = self.get_object(Pessoas, request.data.get("beneficiario_id"))
            if not beneficiario:
                return Response(
                    {"res": "Não existe pessoa com o id informado"},
                    status=st.HTTP_400_BAD_REQUEST,
                )
            ticket.beneficiario = beneficiario
        
        if request.data.get("nao_se_aplica_data_inicio") in ["on","off", True, False]:
            nsaDataInicio = request.data.get("nao_se_aplica_data_inicio")
            if nsaDataInicio == "on":
                nsaDataInicio = True
            elif nsaDataInicio == "off":
                nsaDataInicio = False
            saveDataInicio = nsaDataInicio
            ticket.nao_se_aplica_data_inicio = saveDataInicio

        if request.data.get("nao_se_aplica_data_fim") in ["on","off", True, False]:
            nsaDataFim = request.data.get("nao_se_aplica_data_fim")
            if nsaDataFim == "on":
                nsaDataFim = True
            elif nsaDataFim == "off":
                nsaDataFim = False
            saveDataFim = nsaDataFim
            ticket.nao_se_aplica_data_fim = saveDataFim
        
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
    