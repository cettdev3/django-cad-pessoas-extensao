from django.db import models
from .escola import Escola
from .dpEvento import DpEvento

class DpEventoEscola(models.Model):
    id = models.AutoField(primary_key=True)
    dp_evento = models.ForeignKey(DpEvento, on_delete=models.CASCADE)
    escola = models.ForeignKey(Escola, on_delete=models.CASCADE)
    
    class Meta:
        db_table = 'dp_eventos_escolas'