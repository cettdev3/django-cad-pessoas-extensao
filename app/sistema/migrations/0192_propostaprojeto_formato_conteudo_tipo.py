# Generated by Django 4.2.5 on 2023-10-01 12:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sistema', '0191_anexo_tipo'),
    ]

    operations = [
        migrations.AddField(
            model_name='propostaprojeto',
            name='formato_conteudo_tipo',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
