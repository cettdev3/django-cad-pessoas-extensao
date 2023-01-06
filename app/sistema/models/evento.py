from django.db import models
from ..models.endereco import Endereco
from ..models.cidade import Cidade
from ..models.escola import Escola
class Evento(models.Model):
    # Eventos se tornou ensino, aqui ficam controles de alocação de professores nas escolas
    STATUS_PLANNEJADO = "planejamento"
    STATUS_ANDAMENTO = "andamento"
    STATUS_FINALIZADO = "finalizado"
    STATUS_ADIADO = "adiado"
    STATUS_CANCELADO = "cancelado"
    
    STATUS_COLORS = {
        STATUS_PLANNEJADO: "evt-status-blue",
        STATUS_ANDAMENTO: "evt-status-yellow",
        STATUS_FINALIZADO: "evt-status-green",
        STATUS_ADIADO: "evt-status-orange",
        STATUS_CANCELADO: "evt-status-red",
    }

    id = models.AutoField(primary_key=True)
    data_inicio = models.DateTimeField(null = True)
    data_fim = models.DateTimeField(null = True)
    observacao = models.CharField(null = True, max_length=500)
    status = models.CharField(null = True, max_length=100)
    bairro = models.CharField(null = True, max_length=100) 
    logradouro = models.CharField(null = True, max_length=250) 
    cep = models.CharField(null = True, max_length=100) 
    complemento = models.CharField(null = True, max_length=250)
    cidade = models.ForeignKey(Cidade, on_delete=models.SET_NULL, null=True)
    escola = models.ForeignKey(Escola, on_delete=models.SET_NULL, null=True)

    endereco = models.ForeignKey(Endereco, on_delete=models.SET_NULL, null=True)

    class Meta:
        db_table = 'eventos'

    @property
    def status_class(self):
        if self.status:
            return self.STATUS_COLORS[self.status]
        return "evt-status-gray"
    
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

        if enderecoCompleto:
            return enderecoCompleto
        
        if self.endereco:
            return self.endereco.endereco_completo
        
        return enderecoCompleto