# Generated by Django 4.1.7 on 2023-03-15 20:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sistema', '0076_avaliacao_qtdsalas'),
    ]

    operations = [
        migrations.AddField(
            model_name='avaliacao',
            name='observacaoGeral',
            field=models.TextField(blank=True, null=True),
        ),
    ]
