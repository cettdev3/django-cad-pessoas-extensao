# Generated by Django 4.1.5 on 2023-02-02 13:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sistema', '0064_atividade_departamento'),
    ]

    operations = [
        migrations.AlterField(
            model_name='atividade',
            name='linkDocumentos',
            field=models.CharField(blank=True, max_length=5000, null=True),
        ),
    ]
