from django.db import models
from ..models.membroExecucao import MembroExecucao
from ..models.cidade import Cidade
from ..models.alocacao import Alocacao
from ..models.servicoContratado import ServicoContratado
from datetime import datetime, timedelta
from django.utils import timezone

class Ticket(models.Model):
    STATUS_CRIACAO_PENDENTE = "CRIACAO_PENDENTE"
    STATUS_CRIADO = "CRIADO"
    STATUS_ATRASADO_PARA_CRIACAO = "ATRASADO_PARA_CRIACAO"
    STATUS_PRESTACAO_CONTAS_PENDENTE = "PENDING_PRESTACAO_CONTAS"
    STATUS_PRESTACAO_CONTAS_CRIADA = "PRESTACAO_CONTAS_CREATED"

    TIPO_DIARIA = "diaria"
    TIPO_ADIANTAMENTO = "adiantamento"
    TIPO_ADIANTAMENTO_INSUMO = "adiantamento_insumo"
    TIPO_ADIANTAMENTO_COMBUSTIVEL = "adiantamento_combustivel"
    TIPO_VEICULO = "veiculo"
    TIPO_PASSAGEM = "passagem"
    TIPO_RPA = "rpa"
    TIPO_NAO_SE_APLICA = "nao_se_aplica"

    id = models.AutoField(primary_key=True)
    tipo = models.CharField(null = True, max_length=100)
    status = models.CharField(null = True, max_length=100)
    id_protocolo = models.CharField(null = True, max_length=100)
    membro_execucao =  models.ForeignKey(MembroExecucao, on_delete=models.SET_NULL, null=True)
    alocacao =  models.ForeignKey(Alocacao, on_delete=models.SET_NULL, null=True)
    servico_contratado = models.ForeignKey(ServicoContratado, on_delete=models.SET_NULL, null=True)
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

    class Meta:
        db_table = 'tickets'

    def calculate_status(self):
        entity = self.alocacao.acaoEnsino if self.model == 'alocacao' else self.membro_execucao.evento 
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
        return ""
    
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
        return ""
    
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
        return "Status não identificado"

    @property
    def data_inicio_formatada(self):
        return self.data_inicio.strftime("%d/%m/%Y")
    
    @property
    def data_fim_formatada(self):
        return self.data_fim.strftime("%d/%m/%Y")
    