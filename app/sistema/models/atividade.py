from django.db import models
from .acao import Acao
from .tipoAtividade import TipoAtividade
from .dpEvento import DpEvento
from .membroExecucao import MembroExecucao
from .cidade import Cidade
from .departamento import Departamento
from .atividadeSection import AtividadeSection
from .atividadeCategoria import AtividadeCategoria
from .galeria import Galeria
from .propostaProjeto import PropostaProjeto
from datetime import datetime

class Atividade(models.Model):
    STATUS_PENDENTE = 'pendente'
    STATUS_CONCLUIDO = 'concluido'
    STATUS_CANCELADO = 'cancelado'

    CATEGORIA_TAREFA = 'tarefa'
    CATEGORIA_PROGRAMACAO = 'programacao'
    CATEGORIA_META_EXTENSAO = 'meta_extensao'
    CATEGORIA_REUNIAO = 'reuniao'
    CATEGORIA_MARCO = 'marco'
    CATEGORIA_SUBTAREFAS = 'subtarefa'
    CATEGORIA_ATIVIDADE = 'atividade'
    CATEGORY_CHOICES = (
        (CATEGORIA_TAREFA, 'Tarefa', 'badge-categoria-tarefa'),
        (CATEGORIA_PROGRAMACAO, 'Programação', 'badge-categoria-programacao'),
        (CATEGORIA_META_EXTENSAO, 'Meta de Extens', 'badge-categoria-meta-extensao'),
        (CATEGORIA_REUNIAO, 'Reunião', 'badge-categoria-reuniao'),
        (CATEGORIA_MARCO, 'Marco', 'badge-categoria-marco'),
        (CATEGORIA_SUBTAREFAS, 'Subtarefa', 'badge-categoria-subtarefas'),
        (CATEGORIA_ATIVIDADE, 'Atividade', 'badge-categoria-atividade'),
    )
        

    id = models.AutoField(primary_key=True)
    nome = models.CharField(null = True, blank=True, max_length=500)
    descricao = models.CharField(null = True, blank=True, max_length=5000)
    linkDocumentos = models.CharField(null = True, blank=True, max_length=5000)
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
    quantidadeCertificacoes = models.IntegerField(null = True, blank=True)
    quantidadeMatriculas = models.IntegerField(null = True, blank=True)
    quantidadeAtendimentos = models.IntegerField(null = True, blank=True)
    quantidadeInscricoes = models.IntegerField(null = True, blank=True)
    cargaHoraria = models.FloatField(null = True, blank=True)
    id_protocolo = models.CharField(null = True, blank=True, max_length=100)
    data_realizacao_inicio = models.DateField(null = True, blank=True)
    data_realizacao_fim = models.DateField(null = True, blank=True)
    horario_inicio = models.TimeField(null = True, blank=True)
    horario_fim = models.TimeField(null = True, blank=True)
    valor = models.FloatField(null = True, blank=True)
    galeria = models.ForeignKey(Galeria, on_delete=models.SET_NULL, null=True, blank=True)
    atividade_meta = models.BooleanField(default=False, null = True, blank= True)
    categoria = models.CharField(null = True, blank=True, max_length=100)
    atividadeCategorias = models.ManyToManyField(AtividadeCategoria, blank=True)
    atividadeSection = models.ForeignKey(AtividadeSection, on_delete=models.SET_NULL, null=True, blank=True)
    publico_esperado = models.IntegerField(null = True, blank=True)
    local = models.CharField(null = True, blank=True, max_length=500)
    proposta_projeto = models.ForeignKey(PropostaProjeto, on_delete=models.SET_NULL, null=True, blank=True, related_name='atividades')

    class Meta:
        db_table = 'atividades'
    
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
    def tipo_quantitativo(self):
        if self.quantidadeAtendimentos:
            return "Atendimento"
        elif self.quantidadeCertificacoes:
            return "Certificação"
        elif self.quantidadeInscricoes:
            return "Inscrição"
        elif self.quantidadeMatriculas:
            return "Matrícula"
        else:
            return "Outro"
    
    @property
    def tipo_quantitativo_label(self):
        if self.quantidadeAtendimentos:
            return "Quantidade de Atendimentos"
        elif self.quantidadeCertificacoes:
            return "Quantidade de Certificações"
        elif self.quantidadeInscricoes:   
            return "Quantidade de Inscrições"
        elif self.quantidadeMatriculas:
            return "Quantidade de Matrículas"
        else:
            return "Quantidade de Atendimentos"

    @property
    def tipo_quantitativo_valor(self):
        if self.quantidadeAtendimentos:
            return self.quantidadeAtendimentos
        elif self.quantidadeCertificacoes:
            return self.quantidadeCertificacoes
        elif self.quantidadeInscricoes:
            return self.quantidadeInscricoes
        elif self.quantidadeMatriculas:
            return self.quantidadeMatriculas
        else:
            return 0
        
    @property
    def data_realizacao_inicio_formatada(self):
        if self.data_realizacao_inicio:
            return self.data_realizacao_inicio.strftime("%d/%m/%Y")
        else:
            return ""
    
    @property
    def data_realizacao_fim_formatada(self):
        if self.data_realizacao_fim:
            return self.data_realizacao_fim.strftime("%d/%m/%Y")
        else:
            return ""
        
    @property
    def categoria_label(self):
        if self.categoria:
            for choice in self.CATEGORY_CHOICES:
                if choice[0] == self.categoria:
                    return choice[1]  # Return the label
        return "Atividade"
    
    @property
    def categoria_badge(self):
        if self.categoria:
            for choice in self.CATEGORY_CHOICES:
                if choice[0] == self.categoria:
                    return choice[2]
        return "badge-categoria-atividade"

    property
    def carga_horaria_formatada(self):
        if not self.horario_inicio or not self.horario_fim:
            return None

        dt_inicio = datetime.combine(datetime.today(), self.horario_inicio)
        dt_fim = datetime.combine(datetime.today(), self.horario_fim)

        delta = dt_fim - dt_inicio

        hours, remainder = divmod(delta.seconds, 3600)
        minutes, _ = divmod(remainder, 60)
        strCargaHoraria = ""
        if hours > 0:
            strCargaHoraria += f"{hours}h "
        if minutes > 0:
            strCargaHoraria += f"{minutes}m"
        return strCargaHoraria

    @property
    def carga_horaria_formatada_number(self):
        if not self.horario_inicio or not self.horario_fim:
            return None

        dt_inicio = datetime.combine(datetime.today(), self.horario_inicio)
        dt_fim = datetime.combine(datetime.today(), self.horario_fim)

        delta = dt_fim - dt_inicio

        hours, remainder = divmod(delta.seconds, 3600)
        minutes, _ = divmod(remainder, 60)
        return hours