from django.db import models
from ..models.membroExecucao import MembroExecucao
from ..models.acao import Acao
from ..models.dpEvento import DpEvento
from ..models.cidade import Cidade

# Create your models here.
class Avaliacao(models.Model):
    id = models.AutoField(primary_key=True)
    nome = models.CharField(default=None, blank=True, null = True, max_length=100) 
    endereco = models.CharField(default=None, blank=True, null = True, max_length=100) 
    curso = models.CharField(default=None, blank=True, null = True, max_length=100) 
    qtd_salas = models.CharField(default=None, blank=True, null = True, max_length=100) 
    capacidade = models.CharField(default=None, blank=True, null = True, max_length=100) 
    qtd_cadeiras = models.CharField(default=None, blank=True, null = True, max_length=100) 
    qtd_tomadas = models.CharField(default=None, blank=True, null = True, max_length=100) 
    qtd_janelas = models.CharField(default=None, blank=True, null = True, max_length=100) 
    tipo_climatizacao = models.CharField(default=None, blank=True, null = True, max_length=100) 
    qualidade_iluminacao = models.CharField(default=None, blank=True, null = True, max_length=100) 
    turnos_disponiveis = models.CharField(default=None, blank=True, null = True, max_length=100) 
    qtd_banheiros_masculino = models.CharField(default=None, blank=True, null = True, max_length=100) 
    qtd_banheiros_feminino = models.CharField(default=None, blank=True, null = True, max_length=100) 
    rede_eletrica = models.CharField(default=None, blank=True, null = True, max_length=500) 
    qualidade_bebedouro = models.CharField(default=None, blank=True, null = True, max_length=100) 
    acessibilidade = models.CharField(default=None, blank=True, null = True, max_length=100) 
    internet = models.CharField(default=None, blank=True, null = True, max_length=100) 
    data_show = models.CharField(default=None, blank=True, null = True, max_length=100) 
    limpeza = models.CharField(default=None, blank=True, null = True, max_length=100) 
    link_imagens = models.CharField(default=None, blank=True, null = True, max_length=100) 
    parecer = models.CharField(default=None, blank=True, null = True, max_length=500) 
    obs_parecer = models.CharField(default=None, blank=True, null = True, max_length=500) 
    possui_cozinha = models.CharField(default=None, blank=True, null = True, max_length=100) 
    capacidade_cozinha = models.CharField(default=None, blank=True, null = True, max_length=100) 
    qtd_tomadas_cozinha = models.CharField(default=None, blank=True, null = True, max_length=100) 
    funcionalidade_fogao = models.CharField(default=None, blank=True, null = True, max_length=100) 
    refrigeracao = models.CharField(default=None, blank=True, null = True, max_length=100) 
    gas = models.CharField(default=None, blank=True, null = True, max_length=100) 
    bancadas_mesas = models.CharField(default=None, blank=True, null = True, max_length=100) 
    capacidade_fornos = models.CharField(default=None, blank=True, null = True, max_length=100) 
    qtd_fornos = models.CharField(default=None, blank=True, null = True, max_length=100) 
    ventilacao_cozinha = models.CharField(default=None, blank=True, null = True, max_length=100) 
    torneiras_funcionam = models.CharField(default=None, blank=True, null = True, max_length=100) 
    area_complementar = models.CharField(default=None, blank=True, null = True, max_length=100) 
    observacao_cozinha = models.CharField(default=None, blank=True, null = True, max_length=500) 
    laboratorio_informatica = models.CharField(default=None, blank=True, null = True, max_length=100) 
    qtd_computadores = models.CharField(default=None, blank=True, null = True, max_length=100) 
    cabeamento_internet = models.CharField(default=None, blank=True, null = True, max_length=100) 
    qtd_computadores_wifi = models.CharField(default=None, blank=True, null = True, max_length=100) 
    obs_informatica = models.CharField(default=None, blank=True, null = True, max_length=100) 
    lavatorio = models.CharField(default=None, blank=True, null = True, max_length=100) 
    qtd_lavatorio_sb = models.CharField(default=None, blank=True, null = True, max_length=100) 
    cadeiras_de_sb = models.CharField(default=None, blank=True, null = True, max_length=100) 
    qtd_cadeiras_sb = models.CharField(default=None, blank=True, null = True, max_length=100) 
    cidade = models.CharField(default=None, blank=True, null = True, max_length=100) 
    obsinfra = models.CharField(default=None, blank=True, null = True, max_length=500) 
    cidade_realizacao = models.CharField(default=None, blank=True, null = True, max_length=100) 
    avalLocalEmailAvaliador = models.CharField(default=None, blank=True, null = True, max_length=100) 
    tipoAvaliacao = models.CharField(default=None, blank=True, null = True, max_length=100) 
    endereco_realizacao = models.CharField(default=None, blank=True, null = True, max_length=100) 
    observacao_beleza = models.CharField(default=None, blank=True, null = True, max_length=500) 
    sevicodebeleza = models.CharField(default=None, blank=True, null = True, max_length=100) 
    confeitaria = models.CharField(default=None, blank=True, null = True, max_length=100) 
    UsuariolAvaliador = models.CharField(default=None, blank=True, null = True, max_length=100) 
    avalLocalNomeAvaliador = models.CharField(default=None, blank=True, null = True, max_length=100) 
    infomatica = models.CharField(default=None, blank=True, null = True, max_length=100) 
    
    acao = models.ForeignKey(Acao, on_delete=models.SET_NULL, null=True, blank=True)
    evento = models.ForeignKey(DpEvento, on_delete=models.SET_NULL, null=True, blank= True)
    avaliador = models.ForeignKey(MembroExecucao, on_delete=models.SET_NULL, null=True, blank=True)
    bairro = models.CharField(null = True, max_length=100, blank= True)
    logradouro = models.CharField(null = True, max_length=250, blank= True)
    cep = models.CharField(null = True, max_length=100, blank= True)
    complemento = models.CharField(null = True, max_length=250, blank= True)
    cidade = models.ForeignKey(Cidade, on_delete=models.SET_NULL, null=True, blank= True)

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