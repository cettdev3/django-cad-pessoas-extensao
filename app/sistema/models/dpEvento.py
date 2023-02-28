from django.db import models
from .cidade import Cidade
from .escola import Escola
from .pessoa import Pessoas
from .ensino import Ensino
from datetime import datetime

class DpEvento(models.Model):
    EMPRESTIMO = 'emprestimo'
    CURSO_GPS = 'curso_gps'
    GOIAS_FEITO_A_MAO = 'goias_feito_a_mao'
    FEIRAO  = 'feirao'
    MUTIRAO  = 'mutirao'

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
    acaoEnsino = models.ForeignKey(Ensino, on_delete=models.SET_NULL, null=True, blank= True)
    
    class Meta:
        db_table = 'dp_eventos'

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
        return "Evento não identificado"