from django.db import models
from ..models.membroExecucao import MembroExecucao
from ..models.acao import Acao
from ..models.dpEvento import DpEvento
from datetime import datetime

# Create your models here.
class Avaliacao(models.Model):
    id = models.AutoField(primary_key=True)
    acao = models.ForeignKey(Acao, on_delete=models.SET_NULL, null=True, blank=True)
    evento = models.ForeignKey(DpEvento, on_delete=models.SET_NULL, null=True, blank= True)
    avaliador = models.ForeignKey(MembroExecucao, on_delete=models.SET_NULL, null=True, blank=True)
    bairro = models.CharField(null = True, max_length=100, blank= True)
    logradouro = models.CharField(null = True, max_length=250, blank= True)
    cep = models.CharField(null = True, max_length=100, blank= True)
    complemento = models.CharField(null = True, max_length=250, blank= True)
    
    
    qtdSalas = models.IntegerField(null = True, blank= True)
    qtdSalasUpdatedAt = models.DateTimeField(null = True, blank= True)

    observacaoGeral = models.TextField(null = True, blank= True)
    observacaoGeralUpdatedAt = models.DateTimeField(null = True, blank= True)
    class Meta: 
        db_table = 'avaliacoes'
    
    @property
    def endereco_completo(self):
        enderecoCompleto = "" 
        if self.logradouro:
            enderecoCompleto += self.logradouro
        if self.bairro:
            enderecoCompleto += ", "+self.bairro
        if self.complemento:
            enderecoCompleto += ", "+self.complemento
        if self.cep:
            enderecoCompleto += ". "+self.cep+"."
        return enderecoCompleto
