from django.db import models
from ..models.membroExecucao import MembroExecucao
from ..models.cidade import Cidade
from ..models.alocacao import Alocacao
from ..models.escola import Escola
from ..models.dpEvento import DpEvento
from ..models.departamento import Departamento
from ..models.atividade import Atividade
from ..models.pessoa import Pessoas
from ..models.servicoContratado import ServicoContratado
from datetime import datetime, timedelta
from django.utils import timezone

class Ticket(models.Model):
    STATUS_CRIACAO_PENDENTE = "CRIACAO_PENDENTE" # significa que o ticket foi criado mas ainda não foi criado no sistema externo
    STATUS_CRIADO = "CRIADO" # significa que o ticket foi criado no sistema externo
    STATUS_ATRASADO_PARA_CRIACAO = "ATRASADO_PARA_CRIACAO" # significa que o ticket nao foi criado no sistema externo mas o evento já está próximo
    STATUS_PRESTACAO_CONTAS_PENDENTE = "PENDING_PRESTACAO_CONTAS" # significa que a data do ticket ja passou e o ticket ainda nao foi prestado contas
    STATUS_PRESTACAO_CONTAS_CRIADA = "PRESTACAO_CONTAS_CREATED" # significa que a data do ticket ja passou e o ticket ja foi prestado contas
    STATUS_CANCELADO = "CANCELADO" # significa que o ticket foi cancelado

    TIPO_DIARIA = "diaria"
    TIPO_ADIANTAMENTO = "adiantamento"
    TIPO_ADIANTAMENTO_INSUMO = "adiantamento_insumo"
    TIPO_ADIANTAMENTO_COMBUSTIVEL = "adiantamento_combustivel"
    TIPO_VEICULO = "veiculo"
    TIPO_PASSAGEM = "passagem"
    TIPO_RPA = "rpa"
    TIPO_PRODUTO = "produto"
    TIPO_SERVICO = "servico"
    TIPO_OUTRO = "outro"
    TIPO_NAO_SE_APLICA = "nao_se_aplica"

    TIPOS = [
        TIPO_DIARIA,
        TIPO_ADIANTAMENTO,
        TIPO_ADIANTAMENTO_INSUMO,
        TIPO_ADIANTAMENTO_COMBUSTIVEL,
        TIPO_VEICULO,
        TIPO_PASSAGEM,
        TIPO_RPA,
        TIPO_PRODUTO,
        TIPO_SERVICO,
        TIPO_OUTRO,
        TIPO_NAO_SE_APLICA
    ]

    id = models.AutoField(primary_key=True)
    tipo = models.CharField(null = True, max_length=100)
    status = models.CharField(null = True, max_length=100)
    id_protocolo = models.CharField(null = True, max_length=100)
    membro_execucao =  models.ForeignKey(MembroExecucao, on_delete=models.SET_NULL, null=True)
    alocacao =  models.ForeignKey(Alocacao, on_delete=models.SET_NULL, null=True)
    pessoa = models.ForeignKey(Pessoas, on_delete=models.SET_NULL, null=True)
    escola = models.ForeignKey(Escola, on_delete=models.SET_NULL, null=True)
    atividade = models.ForeignKey(Atividade, on_delete=models.SET_NULL, null=True)
    servico_contratado = models.ForeignKey(ServicoContratado, on_delete=models.SET_NULL, null=True)
    beneficiario = models.ForeignKey(Pessoas, on_delete=models.SET_NULL, null=True, related_name="beneficiario")
    meta = models.JSONField(null = True)
    model = models.CharField(null = True, blank=True, max_length=100)
    data_inicio = models.DateField(null = True, blank= True)
    data_fim = models.DateField(null = True, blank= True)
    nao_se_aplica_data_inicio = models.BooleanField(default=False)
    nao_se_aplica_data_fim = models.BooleanField(default=False)
    bairro = models.CharField(null = True, max_length=100, blank= True)
    logradouro = models.CharField(null = True, max_length=250, blank= True)
    cep = models.CharField(null = True, max_length=100, blank= True)
    complemento = models.CharField(null = True, max_length=250, blank= True)
    cidade = models.ForeignKey(Cidade, on_delete=models.SET_NULL, null=True, blank= True)
    observacao = models.CharField(null = True, max_length=250, blank= True)
    valor_orcado = models.DecimalField(null = True, max_digits=10, decimal_places=2, blank= True)
    valor_executado = models.DecimalField(null = True, max_digits=10, decimal_places=2, blank= True)
    from_export = models.BooleanField(default=False)
    rubrica = models.CharField(null = True, max_length=250, blank= True)
    departamento = models.ForeignKey(Departamento, on_delete=models.SET_NULL, null=True, blank=True)
    solicitante = models.ForeignKey(Pessoas, on_delete=models.SET_NULL, null=True, blank=True, related_name="solicitante")
    data_criacao = models.DateTimeField(null=True, blank=True)
    class Meta:
        db_table = 'tickets'

    def calculate_status(self):
        if self.status == self.STATUS_CANCELADO:
            return self.status

        if self.model == 'pessoa':
            return self.status
        
        entity = None
        if self.model == 'alocacao':
            entity = self.alocacao.acaoEnsino 
        if self.model == 'membro_execucao':
            entity = self.membro_execucao.evento
        if self.model == 'atividade':
            entity = self.atividade.evento
        
        if not entity:
            return self.status
        
        today = timezone.now().date()

        if self.status == self.STATUS_CRIACAO_PENDENTE and entity.data_inicio:
            data_inicio_evento_date = entity.data_inicio.fromisoformat(self.data_fim) if isinstance(entity.data_inicio, str) else entity.data_inicio
            delta = data_inicio_evento_date.date() - today if isinstance(data_inicio_evento_date, datetime) else data_inicio_evento_date - today
            days_until_event_start = delta.days
            if days_until_event_start <= 7:
                return self.STATUS_ATRASADO_PARA_CRIACAO
        if self.status == self.STATUS_CRIADO and self.data_fim:
            data_fim_date = self.data_fim.fromisoformat(self.data_fim) if isinstance(self.data_fim, str) else self.data_fim
            two_days_later = data_fim_date + timedelta(days=2)
            is_after = today > two_days_later
            if is_after:
                return self.STATUS_PRESTACAO_CONTAS_PENDENTE
        return self.status                       
    
    @property
    def status_calculado(self):
        return self.calculate_status()
    
    @property
    def endereco_completo(self):
        enderecoCompleto = "" 
        if self.cidade:
            enderecoCompleto += self.cidade.nome + " GO, "
        if self.logradouro:
            enderecoCompleto += self.logradouro
        if self.bairro:
            enderecoCompleto += ", "+self.bairro
        if self.complemento:
            enderecoCompleto += ", "+self.complemento
        if self.cep:
            enderecoCompleto += ". "+self.cep+"."
        return enderecoCompleto
    
    @property
    def icon(self):
        if self.tipo == self.TIPO_DIARIA:
            return "fa-hotel"
        elif self.tipo == self.TIPO_ADIANTAMENTO:
            return "fa-money-bill"
        elif self.tipo == self.TIPO_ADIANTAMENTO_INSUMO:
            return "fa-cart-shopping"
        elif self.tipo == self.TIPO_ADIANTAMENTO_COMBUSTIVEL:
            return "fa-gas-pump"
        elif self.tipo == self.TIPO_VEICULO:
            return "fa-car"
        elif self.tipo == self.TIPO_PASSAGEM:
            return "fa-bus"
        elif self.tipo == self.TIPO_RPA:
            return "fa-file-contract"
        return "fa-circle-question"
    
    @property
    def tipo_formatado(self):
        if self.tipo == self.TIPO_DIARIA:
            return "Diária"
        elif self.tipo == self.TIPO_ADIANTAMENTO:
            return "Adiantamento"
        elif self.tipo == self.TIPO_ADIANTAMENTO_INSUMO:
            return "Adiantamento de insumo"
        elif self.tipo == self.TIPO_ADIANTAMENTO_COMBUSTIVEL:
            return "Adiantamento de combustível"
        elif self.tipo == self.TIPO_VEICULO:
            return "Veículo"
        elif self.tipo == self.TIPO_PASSAGEM:
            return "Passagem"
        elif self.tipo == self.TIPO_RPA:
            return "RPA"
        elif self.tipo == self.TIPO_PRODUTO:
            return "Compra de produto(s)"
        elif self.tipo == self.TIPO_SERVICO:
            return "Contratação de serviço(s)"
        elif self.tipo == self.TIPO_OUTRO:
            return "Outros"
        return "Não Informado"
    
    @property
    def status_class(self):
        if self.calculate_status() == self.STATUS_ATRASADO_PARA_CRIACAO:
            return "criacao_atrasada"
        elif self.calculate_status() == self.STATUS_PRESTACAO_CONTAS_PENDENTE:
            return "prestacao_pendente"
        elif self.status == self.STATUS_CRIACAO_PENDENTE:
            return "nao_criado"
        elif self.status == self.STATUS_CRIADO:
            return "criado"
        elif self.status == self.STATUS_PRESTACAO_CONTAS_CRIADA:
            return "conta_prestada"  
        elif self.status == self.STATUS_CANCELADO:
            return "cancelado" 
        return ""
    
    @property
    def status_formatado(self):
        if self.calculate_status() == self.STATUS_ATRASADO_PARA_CRIACAO:
            return "Criação de demanda atrasada"
        elif self.calculate_status()  == self.STATUS_PRESTACAO_CONTAS_PENDENTE:
            return "prestação de contas atrasada"
        elif self.status == self.STATUS_PRESTACAO_CONTAS_CRIADA:
            return "Contas prestadas"
        elif self.status == self.STATUS_CRIACAO_PENDENTE:
            return "demanda não criada no protocolo"    
        elif self.status == self.STATUS_CRIADO:
            return "demanda criada no protocolo"
        elif self.status == self.STATUS_CANCELADO:
            return "demanda cancelada"
        return "Status não identificado"

    @property
    def data_inicio_formatada(self):
        return self.data_inicio.strftime("%d/%m/%Y")
    
    @property
    def data_fim_formatada(self):
        return self.data_fim.strftime("%d/%m/%Y")
    
    @property
    def data_criacao_formatada(self):
        data_criacao_local = timezone.localtime(self.data_criacao)

        data_criacao_form = data_criacao_local.strftime("%d/%m/%Y %H:%M:%S")
        return data_criacao_form if self.data_criacao else "Não informado"