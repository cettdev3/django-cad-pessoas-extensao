from django.db import models
from ..models.cidade import Cidade
from ..models.escola import Escola
from ..models.pessoa import Pessoas
from ..models.itinerario import Itinerario

class ItinerarioItem(models.Model):
    id = models.AutoField(primary_key=True)
    data_hora = models.DateField(null = True, blank= True)
    bairro = models.CharField(null = True, max_length=100, blank= True)
    logradouro = models.CharField(null = True, max_length=250, blank= True)
    cep = models.CharField(null = True, max_length=100, blank= True)
    complemento = models.CharField(null = True, max_length=250, blank= True)
    cidade = models.ForeignKey(Cidade, on_delete=models.SET_NULL, null=True, blank= True)
    escola = models.ForeignKey(Escola, on_delete=models.SET_NULL, null=True)
    itinerario = models.ForeignKey(Itinerario, on_delete=models.SET_NULL, null=True, blank= True)
    
    class Meta:
        db_table = 'itinerario_itens'

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