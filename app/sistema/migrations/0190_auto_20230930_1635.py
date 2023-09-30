from django.db import migrations, models

def populate_membroexecucaoroles(apps, schema_editor):
    MembroExecucaoRoles = apps.get_model('sistema', 'MembroExecucaoRoles')
    MembroExecucaoRoles.objects.create(nome="Professor(a)", slug="professor_a")

def reverse(apps, schema_editor):
    pass

class Migration(migrations.Migration):

    dependencies = [
        ('sistema', '0189_alter_atividade_atividadecategorias'),
    ]

    operations = [
        migrations.RunPython(populate_membroexecucaoroles, reverse)
    ]
