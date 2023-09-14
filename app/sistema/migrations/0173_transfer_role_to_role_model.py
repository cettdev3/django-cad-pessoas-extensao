from django.db import migrations, models
import re

def create_slug_from_name(name):
    if not name:
        return None
    
    slug = name.lower()
    
    slug = re.sub(r'[^\w\s]', '', slug)
    
    slug = slug.replace(' ', '_')
    
    return slug

def forward_migration(apps, schema_editor):
    MembroExecucao = apps.get_model('sistema', 'MembroExecucao')
    MembroExecucaoRoles = apps.get_model('sistema', 'MembroExecucaoRoles')

    for membro in MembroExecucao.objects.all():
        if not membro.role:
            continue
        slug = create_slug_from_name(membro.role)
        role, _ = MembroExecucaoRoles.objects.get_or_create(nome=membro.role, defaults={'slug': slug})
        membro.role_model = role
        membro.save()

def backward_migration(apps, schema_editor):
    MembroExecucao = apps.get_model('sistema', 'MembroExecucao')
    MembroExecucaoRoles = apps.get_model('sistema', 'MembroExecucaoRoles')

    for membro in MembroExecucao.objects.all():
        if membro.role_model:
            membro.role = membro.role_model.nome
            membro.save()

    MembroExecucaoRoles.objects.all().delete()

class Migration(migrations.Migration):

    dependencies = [
        ('sistema', '0172_membroexecucao_role_model'),
    ]

    operations = [
        migrations.RunPython(forward_migration, backward_migration)
    ]