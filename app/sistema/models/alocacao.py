from django.db import models
import datetime
from ..models.ensino import Ensino
from ..models.cidade import Cidade
from ..models.pessoa import Pessoas
from ..models.curso import Curso
from ..models.turno import Turno

class Alocacao(models.Model):
    TIPO_COTEC = 'cotec'
    TIPO_RPA = 'rpa'
    TIPO_GPS = 'gps'
    
    TIPO_CHOICES = (
        (TIPO_COTEC, 'COTEC'),
        (TIPO_RPA, 'RPA'),
        (TIPO_GPS, 'GPS'),
    )

    id = models.AutoField(primary_key=True)
    acaoEnsino = models.ForeignKey(Ensino, on_delete=models.SET_NULL, null=True)
    professor = models.ForeignKey(Pessoas, on_delete=models.SET_NULL, null=True) 
    curso = models.ForeignKey(Curso, on_delete=models.SET_NULL, null=True) 
    tipo = models.CharField(null = True, max_length=50)
    data_inicio = models.DateField(null = True)
    data_fim = models.DateField(null = True)
    data_saida = models.DateField(null = True)
    data_retorno = models.DateField(null = True)
    status = models.CharField(null = True, max_length=50)   
    observacao = models.CharField(null = True, max_length=500)
    codigo_siga = models.CharField(null = True, max_length=100)
    quantidade_matriculas = models.IntegerField(null = True)
    bairro = models.CharField(null = True, max_length=100) 
    logradouro = models.CharField(null = True, max_length=250) 
    cep = models.CharField(null = True, max_length=100) 
    complemento = models.CharField(null = True, max_length=250)
    cidade = models.ForeignKey(Cidade, on_delete=models.SET_NULL, null=True)
    turnos = models.ManyToManyField(Turno, blank=True)
    aulas_sabado = models.BooleanField(default=False)
    atividade = models.ForeignKey('Atividade', on_delete=models.SET_NULL, null=True, blank=True, related_name='alocacoes')
    funcao = models.CharField(null = True, max_length=100)
    cargaHoraria = models.FloatField(null = True)
    tipoContratacao = models.CharField(null = True, max_length=100)
    membroExecucao = models.ForeignKey('MembroExecucao', on_delete=models.SET_NULL, null=True, blank=True, related_name='alocacoes')
    class Meta:
        db_table = 'alocacoes'

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
    def data_inicio_formatada(self):
        if self.data_inicio:
            return self.data_inicio.strftime("%d/%m/%Y")
        return None
    
    @property
    def data_fim_formatada(self):
        if self.data_fim:
            return self.data_fim.strftime("%d/%m/%Y")
        return None

    @property
    def tipo_formatado(self):
        if self.tipo:
            if self.tipo == 'cotec':
                return 'COTEC'
            elif self.tipo == 'rpa':
                return 'RPA'
            elif self.tipo == 'gps':
                return 'GPS'
        return "Não Informado"