from django.db import models

from ..models.cidade import Cidade

class Endereco(models.Model):
    id = models.AutoField(primary_key=True)
    bairro = models.CharField(null = True, max_length=100) 
    logradouro = models.CharField(null = True, max_length=250) 
    cep = models.CharField(null = True, max_length=100) 
    complemento = models.CharField(null = True, max_length=250)
    cidade = models.ForeignKey(Cidade, on_delete=models.SET_NULL, null=True)
    class Meta:
        db_table = 'enderecos'
    
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
        return enderecoCompleto