# Generated by Django 4.1.7 on 2023-04-04 18:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sistema', '0083_ticket_nao_se_aplica_data_fim_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='alocacao',
            name='tipo',
            field=models.CharField(max_length=50, null=True),
        ),
    ]
