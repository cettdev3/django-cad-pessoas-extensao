# Generated by Django 4.1.7 on 2023-04-03 18:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sistema', '0082_ticket_observacao'),
    ]

    operations = [
        migrations.AddField(
            model_name='ticket',
            name='nao_se_aplica_data_fim',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='ticket',
            name='nao_se_aplica_data_inicio',
            field=models.BooleanField(default=False),
        ),
    ]
