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
    
    # DADOS GERAIS
    qtdSalas = models.IntegerField(null = True, blank= True)
    qtdSalasUpdatedAt = models.DateTimeField(null = True, blank= True)
    observacaoGeral = models.TextField(null = True, blank= True)
    observacaoGeralUpdatedAt = models.DateTimeField(null = True, blank= True)
    geralTamanhoEspaco = models.CharField(null = True, max_length=100, blank= True)
    geralTamanhoEspacoUpdatedAt = models.DateTimeField(null = True, blank= True)
    geralQuantidadeDataShow = models.IntegerField(null = True, blank= True)
    geralQuantidadeDataShowUpdatedAt = models.DateTimeField(null = True, blank= True)
    geralHasBebedouro = models.CharField(null = True, max_length=100, blank= True)
    geralHasBebedouroUpdatedAt = models.DateTimeField(null = True, blank= True)
    geralHasRedeEletrica = models.CharField(null = True, max_length=100, blank= True)
    geralHasRedeEletricaUpdatedAt = models.DateTimeField(null = True, blank= True)
    geralHasCadeiras = models.CharField(null = True, max_length=100, blank= True)
    geralHasCadeirasUpdatedAt = models.DateTimeField(null = True, blank= True)
    geralHasEquipeLimpeza = models.CharField(null = True, max_length=100, blank= True)
    geralHasEquipeLimpezaUpdatedAt = models.DateTimeField(null = True, blank= True)
    geralHasIluminacao = models.CharField(null = True, max_length=100, blank= True)
    geralHasIluminacaoUpdatedAt = models.DateTimeField(null = True, blank= True)
    geralQuantidadeJanelas = models.IntegerField(null = True, blank= True)
    geralQuantidadeJanelasUpdatedAt = models.DateTimeField(null = True, blank= True)
    geralQuantidadeBanheiros = models.IntegerField(null = True, blank= True)
    geralQuantidadeBanheirosUpdatedAt = models.DateTimeField(null = True, blank= True)

    # SALA DE CULINÀRIA
    salaCulinariaHasEspacoTurmas40Alunos = models.CharField(null = True, max_length=100, blank= True)
    salaCulinariaHasEspacoTurmas40AlunosUpdatedAt = models.DateTimeField(null = True, blank= True)
    salaCulinariaHasVentilacao = models.CharField(null = True, max_length=100, blank= True)
    salaCulinariaHasVentilacaoUpdatedAt = models.DateTimeField(null = True, blank= True)
    salaCulinariaQuantidadeTomadas = models.IntegerField(null = True, blank= True)
    salaCulinariaQuantidadeTomadasUpdatedAt = models.DateTimeField(null = True, blank= True)
    salaCulinariaQuantidadeFogoesFuncionando = models.IntegerField(null = True, blank= True)
    salaCulinariaQuantidadeFogoesFuncionandoUpdatedAt = models.DateTimeField(null = True, blank= True)
    salaCulinariaQuantidadeFornosFuncionando = models.IntegerField(null = True, blank= True)
    salaCulinariaQuantidadeFornosFuncionandoUpdatedAt = models.DateTimeField(null = True, blank= True)
    salaCulinariaHasIluminacaoAdequada = models.CharField(null = True, max_length=100, blank= True)
    salaCulinariaHasIluminacaoAdequadaUpdatedAt = models.DateTimeField(null = True, blank= True)
    salaCulinariaQuantidadeGeladeirasFuncionando = models.IntegerField(null = True, blank= True)
    salaCulinariaQuantidadeGeladeirasFuncionandoUpdatedAt = models.DateTimeField(null = True, blank= True)
    salaCulinariaQuantidadeMesasBancadas = models.IntegerField(null = True, blank= True)
    salaCulinariaQuantidadeMesasBancadasUpdatedAt = models.DateTimeField(null = True, blank= True)
    salaCulinariaQuantidadePiasComTorneiraFuncionando = models.IntegerField(null = True, blank= True)
    salaCulinariaQuantidadePiasComTorneiraFuncionandoUpdatedAt = models.DateTimeField(null = True, blank= True)
    salaCulinariaQuantidadeVasilhamesGasComGas = models.IntegerField(null = True, blank= True)
    salaCulinariaQuantidadeVasilhamesGasComGasUpdatedAt = models.DateTimeField(null = True, blank= True)
    salaCulinariaQuantidadeVasilhamesGasVazios = models.IntegerField(null = True, blank= True)
    salaCulinariaQuantidadeVasilhamesGasVaziosUpdatedAt = models.DateTimeField(null = True, blank= True)
    salaCulinariaObservacao = models.TextField(null = True, blank= True)
    salaCulinariaObservacaoUpdatedAt = models.DateTimeField(null = True, blank= True)

    # SALA DE CURSOS DE BELEZA
    salaServicosBelezaHasPontoAguaExterno = models.CharField(null = True, max_length=100, blank= True)
    salaServicosBelezaHasPontoAguaExternoUpdatedAt = models.DateTimeField(null = True, blank= True)
    salaServicosBelezaQuantidadePiasHigienizacao = models.IntegerField(null = True, blank= True)
    salaServicosBelezaQuantidadePiasHigienizacaoUpdatedAt = models.DateTimeField(null = True, blank= True)
    salaServicosBelezaQuantidadeCadeirasSalao = models.IntegerField(null = True, blank= True)
    salaServicosBelezaQuantidadeCadeirasSalaoUpdatedAt = models.DateTimeField(null = True, blank= True)
    salaServicosBelezaObservacao = models.TextField(null = True, blank= True)
    salaServicosBelezaObservacaoUpdatedAt = models.DateTimeField(null = True, blank= True)
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
