# Generated by Django 4.2.3 on 2023-07-19 15:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sistema', '0140_pessoas_instituicao_alter_atividade_descricao'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pessoas',
            name='instituicao',
            field=models.CharField(blank=True, choices=[('escola', 'Escola'), ('cett', 'CETT'), ('outros', 'Outros')], max_length=50, null=True),
        ),
    ]
