from django.db import models
from sistema.models import Pessoas, PropostaProjeto
from django.utils import timezone

class Comentario(models.Model):
    id = models.AutoField(primary_key=True)
    conteudo = models.TextField(null = True)
    autor = models.ForeignKey(Pessoas, on_delete=models.SET_NULL, null=True, blank=True, related_name='comentarios')
    proposta_projeto = models.ForeignKey(PropostaProjeto, on_delete=models.SET_NULL, null=True, blank=True, related_name='comentarios')
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = 'comentarios'

    @property
    def created_at_formatado(self):
        created_at = timezone.localtime(self.created_at)
        return created_at.strftime("%d/%m/%Y %H:%M:%S")