from django.db import models
from ..models.cidade import Cidade
from ..models.pessoa import Pessoas
from ..models.acao import Acao
from ..models.dpEvento import DpEvento
from ..models.itinerario import Itinerario

class MembroExecucao(models.Model):    
    id = models.AutoField(primary_key=True)
    data_inicio = models.DateField(null = True, blank= True)
    data_fim = models.DateField(null = True, blank= True)
    bairro = models.CharField(null = True, max_length=100, blank= True)
    tipo = models.CharField(null = True, max_length=100, blank= True)
    logradouro = models.CharField(null = True, max_length=250, blank= True)
    cep = models.CharField(null = True, max_length=100, blank= True)
    complemento = models.CharField(null = True, max_length=250, blank= True)
    cidade = models.ForeignKey(Cidade, on_delete=models.SET_NULL, null=True, blank= True)
    pessoa = models.ForeignKey(Pessoas, on_delete=models.SET_NULL, null=True, blank= True)
    acao = models.ForeignKey(Acao, on_delete=models.SET_NULL, null=True, blank= True)
    evento = models.ForeignKey(DpEvento, on_delete=models.SET_NULL, null=True, blank= True)
    itinerario = models.ForeignKey(Itinerario, on_delete=models.SET_NULL, null=True, blank= True)
    avaliador = models.BooleanField(default=False, null = True, blank= True)
    observacao = models.CharField(null = True, max_length=250, blank= True)

    class Meta:
        db_table = 'membros_execucao'
    
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
    def ticket_status(self):
        tickets = self.ticket_set.all()
        if tickets and len(tickets) > 0:
            for ticket in tickets:
                if ticket.status == "CRIACAO_PENDENTE":
                    return "pendente"
        else: 
            return "sem_tickets"
        return "criado"
