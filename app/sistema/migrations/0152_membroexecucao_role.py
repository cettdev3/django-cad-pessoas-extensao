# Generated by Django 4.2.3 on 2023-07-21 20:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sistema', '0151_alter_atividade_atividadecategorias'),
    ]

    operations = [
        migrations.AddField(
            model_name='membroexecucao',
            name='role',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
