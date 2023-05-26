from django.db import models

class TipoAtividade(models.Model):
    id = models.AutoField(primary_key=True)
    nome = models.CharField(null = True, max_length=250)   
    descricao = models.CharField(null = True, blank=True, max_length=2000)
    categoria = models.CharField(null = True, blank=True, max_length=50)

    class Meta:
        db_table = 'tipos_atividades'