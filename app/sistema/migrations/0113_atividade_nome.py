# Generated by Django 4.2.1 on 2023-05-15 13:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sistema', '0112_atividade_atividadesection'),
    ]

    operations = [
        migrations.AddField(
            model_name='atividade',
            name='nome',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
