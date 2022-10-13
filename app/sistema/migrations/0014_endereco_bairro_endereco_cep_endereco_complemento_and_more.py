# Generated by Django 4.1.2 on 2022-10-13 11:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sistema', '0013_evento_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='endereco',
            name='bairro',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='endereco',
            name='cep',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='endereco',
            name='complemento',
            field=models.CharField(max_length=250, null=True),
        ),
        migrations.AddField(
            model_name='endereco',
            name='logradouro',
            field=models.CharField(max_length=250, null=True),
        ),
    ]
