from django.db import models
from itertools import chain
from django.utils import timezone

class PropostaProjeto(models.Model):
    STATUS_RASCUNHO = "rascunho"
    STATUS_EM_ANALISE = "em_analise"
    STATUS_EM_ANALISE_DIRECAO = "em_analise_direcao"
    STATUS_EM_ANALISE_CETT = "em_analise_cett"
    STATUS_DEVOLVIDA = "devolvida"
    STATUS_APROVADA = "aprovada"
    STATUS_REPROVADA = "reprovada"
    STATUS_CANCELADA = "cancelada"
    STATUS_SOLICITAR_MUDANCA = "solicitar_mudanca"
    STATUS_DEVOLVIDA_APOS_APROVACAO = "devolvida_apos_aprovacao"

    STATUS_CHOICES = [
        (STATUS_RASCUNHO, 'Rascunho'),
        (STATUS_EM_ANALISE, 'Em análise'),
        (STATUS_EM_ANALISE_DIRECAO, 'Em análise pela direção'),
        (STATUS_EM_ANALISE_CETT, 'Em análise pelo CETT'),
        (STATUS_DEVOLVIDA, 'Devolvida'),
        (STATUS_APROVADA, 'Aprovada'),
        (STATUS_REPROVADA, 'Reprovada'),
        (STATUS_CANCELADA, 'Cancelada'),
        (STATUS_SOLICITAR_MUDANCA, 'Mudança solicitada'),
        (STATUS_DEVOLVIDA_APOS_APROVACAO, 'Devolvida após aprovação'),
    ]
    
    STATUS_MENU_LABEL = [
        (STATUS_RASCUNHO, 'Em elaboração'),
        (STATUS_EM_ANALISE, 'Submeter para análise'),
        (STATUS_EM_ANALISE_DIRECAO, 'Submeter para análise da direção'),
        (STATUS_EM_ANALISE_CETT, 'Submeter para análise do CETT'),
        (STATUS_DEVOLVIDA, 'Devolver para o autor'),
        (STATUS_APROVADA, 'Aprovar'),
        (STATUS_REPROVADA, 'Reprovar'),
        (STATUS_CANCELADA, 'Cancelar'),
        (STATUS_SOLICITAR_MUDANCA, 'Solicitar mudança'),
        (STATUS_DEVOLVIDA_APOS_APROVACAO, 'Devolver ao autor após aprovação'),
    ]

    titulo_projeto = models.CharField(max_length=255, null=True, blank=True)
    data_inicio = models.DateField(null=True, blank=True)
    data_fim = models.DateField(null=True, blank=True)
    resumo_proposta = models.TextField(null=True, blank=True)
    objetivos_gerais = models.TextField(null=True, blank=True)
    objetivos_especificos = models.TextField(null=True, blank=True)
    metodologia = models.TextField(null=True, blank=True)
    formato_conteudo = models.TextField(null=True, blank=True)
    justificativas = models.TextField(null=True, blank=True)
    resultados_esperados = models.TextField(null=True, blank=True)
    fontes_apoio = models.TextField(null=True, blank=True)
    informacoes_adicionais = models.TextField(null=True, blank=True)
    publico_alvo = models.TextField(null=True, blank=True)
    orcamento = models.ForeignKey("Orcamento", on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=255, choices=STATUS_CHOICES, default='em_analise')
    escola = models.ForeignKey("Escola", on_delete=models.SET_NULL, null=True, blank=True)
  
    class Meta:
        db_table = 'propostas_projeto'

    @property
    def responsaveis(self):
        return self.equipe.filter(role__slug='responsavel')
    
    @property
    def proponentes(self):
        return self.equipe.filter(role__slug='proponente')

    @property
    def status_formatado(self):
        return dict(self.STATUS_CHOICES)[self.status]
   
    @property
    def status_menu_label(self):
        return dict(self.STATUS_MENU_LABEL)[self.status]
    
    @property
    def read_only(self):
        readOnly =  self.status != self.STATUS_RASCUNHO
        readOnly = readOnly and self.status != self.STATUS_DEVOLVIDA 
        readOnly = readOnly and self.status != self.STATUS_DEVOLVIDA_APOS_APROVACAO
        return readOnly
    
    @property
    def is_editable(self):
        return self.status == self.STATUS_RASCUNHO or self.status == self.STATUS_DEVOLVIDA or self.status == self.STATUS_DEVOLVIDA_APOS_APROVACAO
    
    @property
    def is_deleteable(self):
        return self.status == self.STATUS_RASCUNHO
