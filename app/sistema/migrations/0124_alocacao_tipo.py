# Generated by Django 4.2.1 on 2023-05-25 14:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sistema', '0123_alter_atividade_descricao_alter_atividade_nome'),
    ]

    operations = [
        migrations.AddField(
            model_name='alocacao',
            name='tipo',
            field=models.CharField(max_length=50, null=True),
        ),
    ]
