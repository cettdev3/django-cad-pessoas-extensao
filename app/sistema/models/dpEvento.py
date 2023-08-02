from django.db import models
from .cidade import Cidade
from .escola import Escola
from .alocacao import Alocacao
from .ensino import Ensino
from .propostaProjeto import PropostaProjeto
from itertools import chain

class DpEvento(models.Model):
    EMPRESTIMO = 'emprestimo'
    CURSO_GPS = 'curso_gps'
    GOIAS_FEITO_A_MAO = 'goias_feito_a_mao'
    FEIRAO  = 'feirao'
    MUTIRAO  = 'mutirao'
    RECICLA_GOIAS  = 'recicla_goias'
    PAUTA_POSITIVA  = 'pauta_positiva'
    FEIRA_AGRO_CENTRO_OESTE  = 'feira_agro_centro_oeste'
    DIA_MULHERES  = 'dia_mulheres'
    OPEN_DAY  = 'open_day'
    OUTRO = 'outro'

    MAPPED_TIPOS = [
        EMPRESTIMO
    ]

    STATUS_WAITING_TICKET = 'waiting_ticket'
    STATUS_WAITING_RETURN = 'waiting_return'

    id = models.AutoField(primary_key=True)
    tipo = models.CharField(null = True, blank= True, max_length=50)   
    process_instance = models.CharField(null = True, blank= True, max_length=300)
    variaveis = models.JSONField(null = True, blank= True)
    status = models.CharField(null = True, max_length=50, blank= True)
    descricao = models.CharField(null = True, max_length=1000, blank= True)
    data_inicio = models.DateField(null = True, blank= True)
    data_fim = models.DateField(null = True, blank= True)
    bairro = models.CharField(null = True, max_length=100, blank= True)
    logradouro = models.CharField(null = True, max_length=250, blank= True)
    cep = models.CharField(null = True, max_length=100, blank= True)
    complemento = models.CharField(null = True, max_length=250, blank= True)
    cidade = models.ForeignKey(Cidade, on_delete=models.SET_NULL, null=True, blank= True)
    escola = models.ForeignKey(Escola, on_delete=models.SET_NULL, null=True)
    escolas = models.ManyToManyField(Escola, through='DpEventoEscola', blank=True, related_name='escolas')
    acaoEnsino = models.ForeignKey(Ensino, on_delete=models.SET_NULL, null=True, blank= True)
    horarioInicio = models.TimeField(null = True, blank= True)
    horarioFim = models.TimeField(null = True, blank= True)
    edicao = models.CharField(null = True, max_length=100, blank= True)
    proposta_projeto = models.OneToOneField(PropostaProjeto, on_delete=models.SET_NULL, null=True, blank= True, related_name='evento')
    class Meta:
        db_table = 'dp_eventos'

    @property
    def endereco_completo(self):
        enderecoCompleto = "" 
        if self.cidade and self.cidade.nome != "None" and self.cidade.nome != "":
            enderecoCompleto += self.cidade.nome + " GO, "
        if self.logradouro and self.logradouro != "None" and self.logradouro != "":
            enderecoCompleto += self.logradouro
        if self.bairro and self.bairro != "None" and self.bairro != "":
            enderecoCompleto += ", "+self.bairro
        if self.complemento and self.complemento != "None" and self.complemento != "":
            enderecoCompleto += ", "+self.complemento
        if self.cep and self.cep != "None" and self.cep != "":
            enderecoCompleto += ". "+self.cep+"."
        return enderecoCompleto
    
    @property
    def extrato(self, format='html'):
        extrato = "" 
        if self.endereco_completo:
            extrato += "<div><strong>Endereço</strong> : "+self.cidade.nome + " GO, " + self.endereco_completo + "</div>"
        membrosEquipeExecucao = DpEvento.objects.prefetch_related("membroexecucao_set")
        membrosEquipeExecucao = membrosEquipeExecucao.filter(id=self.id).first().membroexecucao_set.all()
        if self.descricao:
            extrato += "<div><strong>descricao</strong>: " + self.descricao + "</div><hr>"
        for membro in membrosEquipeExecucao:
            extrato += "<div>"
            if membro.pessoa:
                extrato += "<strong>nome beneficiado</strong>: " + membro.pessoa.nome + "<br>"
            if membro.tipo:
                extrato += "<strong>tipo</strong>: " + membro.tipo + "<br>"
            if membro.data_inicio:
                extrato += "<strong>data inicio</strong>: " + membro.data_inicio.strftime("%d/%m/%Y") + "<br>"
            if membro.data_fim:
                extrato += "<strong>data fim</strong>: " + membro.data_fim.strftime("%d/%m/%Y") + "<br>"
            extrato += "</div><hr>"
        return extrato
    
    @property
    def data_inicio_formatada(self):
        return self.data_inicio.strftime("%d/%m/%Y")
    
    @property
    def data_fim_formatada(self):
        return self.data_fim.strftime("%d/%m/%Y")
    
    @property
    def tipo_formatado(self):
        if self.tipo == self.EMPRESTIMO:
            return "Empréstimo"
        elif self.tipo == self.CURSO_GPS:
            return "Curso GPS"
        elif self.tipo == self.FEIRAO:
            return "Feirão do Emprego"
        elif self.tipo == self.GOIAS_FEITO_A_MAO:
            return "Goiás Feito a Mão"
        elif self.tipo == self.MUTIRAO:
            return "Mutirão"
        elif self.tipo == self.OUTRO:
            return "Outro"
        elif self.tipo == self.RECICLA_GOIAS:
            return "Recicla Goiás"
        elif self.tipo == self.FEIRA_AGRO_CENTRO_OESTE:
            return "Feira Agro Centro Oeste"
        elif self.tipo == self.PAUTA_POSITIVA:
            return "Pauta Positiva"
        elif self.tipo == self.DIA_MULHERES:
            return "Dias das Mulheres"
        elif self.tipo == self.OPEN_DAY:
            return "Open Day"
        elif self.tipo:
            return self.tipo
        return "Evento não identificado"
    
    @property
    def membro_execucao_status(self):
        membrosEquipeExecucao = self.membroexecucao_set.all()
        for membro in membrosEquipeExecucao:
            if membro.ticket_status == "pendente":
                return "pendente"
        return "concluido"
    
    @property
    def valor_total(self):
        membro_execucao_objs = self.membroexecucao_set.all()
        ensino_objs = Ensino.objects.filter(dpevento__id=self.id)
        alocacao_objs = Alocacao.objects.filter(acaoEnsino__in=ensino_objs)
        atividade_objs = self.atividade_set.all()

        tickets_membro_execucao = []
        valor_total_membro_execucao = 0
        tickets_alocacao = []
        valor_total_alocacao = 0
        tickets_atividade = []
        valor_total_atividade = 0
        processedIds = []
        for membro_execucao in membro_execucao_objs:
            tickets_membro_execucao = membro_execucao.ticket_set.all()
            for ticket in tickets_membro_execucao:
                if ticket.id in processedIds:
                    continue
                valor_total_membro_execucao += ticket.valor_executado if ticket.valor_executado else 0
                processedIds.append(ticket.id)
        for alocacao in alocacao_objs:
            tickets_alocacao = alocacao.ticket_set.all()
            for ticket in tickets_alocacao:
                if ticket.id in processedIds:
                    continue
                valor_total_alocacao += ticket.valor_executado if ticket.valor_executado else 0
                processedIds.append(ticket.id)
        for atividade in atividade_objs:
            tickets_atividade = atividade.ticket_set.all()
            for ticket in tickets_atividade:
                if ticket.id in processedIds:
                    continue
                valor_total_atividade += ticket.valor_executado if ticket.valor_executado else 0
                processedIds.append(ticket.id)
        return valor_total_membro_execucao + valor_total_alocacao + valor_total_atividade