from django.db import models
from itertools import chain
from django.utils import timezone

class PropostaProjeto(models.Model):
    STATUS_CHOICES = [
        ('em_analise', 'Em análise'),
        ('devolvida', 'Devolvida'),
        ('aprovada', 'Aprovada'),
        ('reprovada', 'Reprovada'),
        ('cancelada', 'Cancelada'),
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
        return self.equipe.filter(role='responsavel')
    
    @property
    def proponentes(self):
        return self.equipe.filter(role='proponente')

    @property
    def status_formatado(self):
        return dict(self.STATUS_CHOICES)[self.status]