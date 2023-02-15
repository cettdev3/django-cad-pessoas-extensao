from django.db import models
from ..models.membroExecucao import MembroExecucao
from ..models.acao import Acao
from ..models.dpEvento import DpEvento
from ..models.cidade import Cidade

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
    # cidade = models.ForeignKey(Cidade, on_delete=models.SET_NULL, null=True, blank= True)

    class Meta:
        db_table = 'avaliacoes'
    
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