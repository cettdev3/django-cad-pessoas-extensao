from django.db import models

class MembroExecucaoRoles(models.Model): 
    SLUG_PROPONENTE = 'proponente'
    SLUG_RESPONSAVEL = 'responsavel'
    SLUG_PRFESSOR = 'professor_a'

    id = models.AutoField(primary_key=True)
    nome = models.CharField(null = True, max_length=100, blank= True)
    slug = models.CharField(null = True, max_length=100, blank= True)
    
    class Meta:
        db_table = 'membro_execucao_roles'
