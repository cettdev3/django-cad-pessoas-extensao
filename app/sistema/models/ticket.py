from django.db import models
from ..models.membroExecucao import MembroExecucao
from ..models.cidade import Cidade
from ..models.alocacao import Alocacao

class Ticket(models.Model):
    STATUS_CREATED = "CREATED"
    STATUS_ATRASADO = "ATRASADO"
    STATUS_EM_DIAS = "EM_DIAS"

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
        if self.status == self.STATUS_CREATED:
            return "created"
        elif self.status == self.STATUS_ATRASADO:
            return "late"
        elif self.status == self.STATUS_EM_DIAS:
            return "in_progress"    
        return ""
    
    @property
    def status_formatado(self):
        if self.status == self.STATUS_CREATED:
            return "demanda criada no protocolo"
        elif self.status == self.STATUS_ATRASADO:
            return "demanda em atraso"
        elif self.status == self.STATUS_EM_DIAS:
            return "demanda não criada no protocolo"    
        return ""

    @property
    def data_inicio_formatada(self):
        return self.data_inicio.strftime("%d/%m/%Y")
    
    @property
    def data_fim_formatada(self):
        return self.data_fim.strftime("%d/%m/%Y")
    