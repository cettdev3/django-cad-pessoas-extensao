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

    atributes_description = {
        'acao': 'Ação',
        'evento': 'Evento',
        'avaliador': 'Avaliador',
        'bairro': 'Bairro',
        'logradouro': 'Logradouro',
        'cep': 'CEP',
        'complemento': 'Complemento',
        'qtdSalas': 'Quantidade de salas',
        'qtdSalasUpdatedAt': 'Data de atualização da quantidade de salas',
        'observacaoGeral': 'Observação geral',
        'observacaoGeralUpdatedAt': 'Data de atualização da observação geral',
        'geralTamanhoEspaco': 'Tamanho do espaço',
        'geralTamanhoEspacoUpdatedAt': 'Data de atualização do tamanho do espaço',
        'geralQuantidadeDataShow': 'Quantidade de projetores',
        'geralQuantidadeDataShowUpdatedAt': 'Data de atualização da quantidade de projetores',
        'geralHasBebedouro': 'Possui bebedouro',
        'geralHasBebedouroUpdatedAt': 'Data de atualização da informação de bebedouro',
        'geralHasRedeEletrica': 'Possui rede elétrica',
        'geralHasRedeEletricaUpdatedAt': 'Data de atualização da informação de rede elétrica',
        'geralHasCadeiras': 'Possui cadeiras',
        'geralHasCadeirasUpdatedAt': 'Data de atualização da informação de cadeiras',
        'geralHasEquipeLimpeza': 'Possui equipe de limpeza',
        'geralHasEquipeLimpezaUpdatedAt': 'Data de atualização da informação de equipe de limpeza',
        'geralHasIluminacao': 'Possui iluminação',
        'geralHasIluminacaoUpdatedAt': 'Data de atualização da informação de iluminação',
        'geralQuantidadeJanelas': 'Quantidade de janelas',
        'geralQuantidadeJanelasUpdatedAt': 'Data de atualização da quantidade de janelas',
        'geralQuantidadeBanheiros': 'Quantidade de banheiros',
        'geralQuantidadeBanheirosUpdatedAt': 'Data de atualização da quantidade de banheiros',
        'salaCulinariaHasEspacoTurmas40Alunos': 'Possui espaço para turmas de 40 alunos',
        'salaCulinariaHasEspacoTurmas40AlunosUpdatedAt': 'Data de atualização da informação sobre o espaço para turmas de 40 alunos',
        'salaCulinariaHasVentilacao': 'Possui ventilação',
        'salaCulinariaHasVentilacaoUpdatedAt': 'Data de atualização da informação sobre a ventilação',
        'salaCulinariaQuantidadeTomadas': 'Quantidade de tomadas',
        'salaCulinariaQuantidadeTomadasUpdatedAt': 'Data de atualização da quantidade de tomadas',
        'salaCulinariaQuantidadeFogoesFuncionando': 'Quantidade de fogões funcionando',
        'salaCulinariaQuantidadeFogoesFuncionandoUpdatedAt': 'Data de atualização da quantidade de fogões funcionando',
        'salaCulinariaQuantidadeFornosFuncionando': 'Quantidade de fornos funcionando',
        'salaCulinariaQuantidadeFornosFuncionandoUpdatedAt': 'Data de atualização da quantidade de fornos funcionando',
        'salaCulinariaHasIluminacaoAdequada': 'Possui iluminação adequada',
        'salaCulinariaHasIluminacaoAdequadaUpdatedAt': 'Data de atualização da informação sobre a iluminação adequada',
        'salaCulinariaQuantidadeGeladeirasFuncionando': 'Quantidade de geladeiras funcionando',
        'salaCulinariaQuantidadeGeladeirasFuncionandoUpdatedAt': 'Data de atualização da quantidade de geladeiras funcionando',
        'salaCulinariaQuantidadeMesasBancadas': 'Quantidade de mesas/bancadas',
        'salaCulinariaQuantidadeMesasBancadasUpdatedAt': 'Data de atualização da quantidade de mesas/bancadas',
        'salaCulinariaQuantidadePiasComTorneiraFuncionando': 'Quantidade de pias com torneira funcionando',
        'salaCulinariaQuantidadePiasComTorneiraFuncionandoUpdatedAt': 'Data de atualização da quantidade de pias com torneira funcionando',
        'salaCulinariaQuantidadeVasilhamesGasComGas': 'Quantidade de vasilhames de gás com gás',
        'salaCulinariaQuantidadeVasilhamesGasComGasUpdatedAt': 'Data de atualização da quantidade de vasilhames de gás com gás',
        'salaCulinariaQuantidadeVasilhamesGasVazios': 'Quantidade de vasilhames de gás vazios',
        'salaCulinariaQuantidadeVasilhamesGasVaziosUpdatedAt': 'Data de atualização da quantidade de vasilhames de gás vazios',
        'salaCulinariaObservacao': 'Observação da sala culinária',
        'salaCulinariaObservacaoUpdatedAt': 'Data de atualização da observação da sala culinária',
        'salaServicosBelezaHasPontoAguaExterno': 'Possui ponto de água externo',
        'salaServicosBelezaHasPontoAguaExternoUpdatedAt': 'Data de atualização da informação sobre o ponto de água externo',
        'salaServicosBelezaQuantidadePiasHigienizacao': 'Quantidade de pias para higienização',
        'salaServicosBelezaQuantidadePiasHigienizacaoUpdatedAt': 'Data de atualização da quantidade de pias para higienização',
        'salaServicosBelezaQuantidadeCadeirasSalao': 'Quantidade de cadeiras do salão',
        'salaServicosBelezaQuantidadeCadeirasSalaoUpdatedAt': 'Data de atualização da quantidade de cadeiras do salão',
        'salaServicosBelezaObservacao': 'Observação da sala de serviços de beleza',
        'salaServicosBelezaObservacaoUpdatedAt': 'Data de atualização da observação da sala de serviços de beleza',

    }
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