from django.db import models
from ..models.endereco import Endereco

class Evento(models.Model):
    STATUS_PLANNEJADO = "planejamento"
    STATUS_ANDAMENTO = "andamento"
    STATUS_FINALIZADO = "finalizado"
    STATUS_ADIADO = "adiado"
    
    STATUS_COLORS = {
        STATUS_PLANNEJADO: "evt-status-blue",
        STATUS_ANDAMENTO: "evt-status-yellow",
        STATUS_FINALIZADO: "evt-status-green",
        STATUS_ADIADO: "evt-status-red"
    }

    id = models.AutoField(primary_key=True)
    data_inicio = models.DateTimeField(null = True)
    data_fim = models.DateTimeField(null = True)
    observacao = models.CharField(null = True, max_length=500)
    status = models.CharField(null = True, max_length=100)
    endereco = models.ForeignKey(Endereco, on_delete=models.SET_NULL, null=True)

    class Meta:
        db_table = 'eventos'

    @property
    def status_class(self):
        if self.status:
            return self.STATUS_COLORS[self.status]
        return "evt-status-gray"