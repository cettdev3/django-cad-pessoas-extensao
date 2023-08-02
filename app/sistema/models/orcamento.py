from django.db import models

class Orcamento(models.Model):
    id = models.AutoField(primary_key=True)
    
    class Meta:
        db_table = 'orcamentos'
