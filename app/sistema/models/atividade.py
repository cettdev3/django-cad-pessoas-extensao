from django.db import models
from .acao import Acao
from .tipoAtividade import TipoAtividade
from .dpEvento import DpEvento
from .membroExecucao import MembroExecucao
from .cidade import Cidade
from .departamento import Departamento

class Atividade(models.Model):
    id = models.AutoField(primary_key=True)
    descricao = models.CharField(null = True, blank=True, max_length=300)
    linkDocumentos = models.CharField(null = True, blank=True, max_length=300)
    status = models.CharField(null = True, blank=True, max_length=50)
    acao = models.ForeignKey(Acao, on_delete=models.SET_NULL, null=True, blank=True)
    evento = models.ForeignKey(DpEvento, on_delete=models.SET_NULL, null=True, blank= True)
    tipoAtividade = models.ForeignKey(TipoAtividade, on_delete=models.SET_NULL, null=True, blank=True)
    responsavel = models.ForeignKey(MembroExecucao, on_delete=models.SET_NULL, null=True, blank=True)
    departamento = models.ForeignKey(Departamento, on_delete=models.SET_NULL, null=True, blank=True)
    cidade = models.ForeignKey(Cidade, on_delete=models.SET_NULL, null=True, blank=True)
    logradouro = models.CharField(null = True, blank=True, max_length=100)
    bairro = models.CharField(null = True, blank=True, max_length=100)
    cep = models.CharField(null = True, blank=True, max_length=20)
    complemento = models.CharField(null = True, blank=True, max_length=250)

    class Meta:
        db_table = 'atividades'