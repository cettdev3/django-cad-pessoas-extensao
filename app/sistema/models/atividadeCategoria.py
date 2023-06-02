from django.db import models

class AtividadeCategoria(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, unique=True, null=True, blank=True)
    description = models.CharField(null = True, blank=True, max_length=500)
    badge = models.CharField(max_length=100, unique=True, null=True, blank=True)
    slug = models.CharField(max_length=100, unique=True, null=True, blank=True)

    class Meta:
        db_table = 'atividade_categorias'
    
    def __str__(self):
        return self.name

