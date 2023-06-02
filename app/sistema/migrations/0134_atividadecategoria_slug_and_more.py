# Generated by Django 4.2.1 on 2023-06-02 12:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sistema', '0133_atividade_atividadecategorias'),
    ]

    operations = [
        migrations.AddField(
            model_name='atividadecategoria',
            name='slug',
            field=models.CharField(blank=True, max_length=100, null=True, unique=True),
        ),
        migrations.AlterField(
            model_name='atividadecategoria',
            name='badge',
            field=models.CharField(blank=True, max_length=100, null=True, unique=True),
        ),
        migrations.AlterField(
            model_name='atividadecategoria',
            name='name',
            field=models.CharField(blank=True, max_length=100, null=True, unique=True),
        ),
    ]
