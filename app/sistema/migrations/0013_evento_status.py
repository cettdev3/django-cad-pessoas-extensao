# Generated by Django 4.1.2 on 2022-10-11 19:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sistema', '0012_remove_pessoas_endereco_pessoas_bairro_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='evento',
            name='status',
            field=models.CharField(max_length=100, null=True),
        ),
    ]
