# Generated by Django 4.1.5 on 2023-02-02 14:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sistema', '0065_alter_atividade_linkdocumentos'),
    ]

    operations = [
        migrations.AddField(
            model_name='ensino',
            name='tipo',
            field=models.CharField(max_length=100, null=True),
        ),
    ]
