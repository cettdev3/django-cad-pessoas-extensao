# Generated by Django 4.2.3 on 2023-07-27 12:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sistema', '0158_alter_orcamentoitem_descricao_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='propostaprojeto',
            name='publico_alvo',
            field=models.TextField(blank=True, null=True),
        ),
    ]
