# Generated by Django 4.2.5 on 2023-09-18 18:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sistema', '0186_alter_alocacao_atividade_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='alocacao',
            name='numero_matricula',
            field=models.CharField(max_length=100, null=True),
        ),
    ]
