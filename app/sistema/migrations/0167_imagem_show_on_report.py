# Generated by Django 4.2.4 on 2023-08-07 13:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sistema', '0166_alter_dpevento_proposta_projeto'),
    ]

    operations = [
        migrations.AddField(
            model_name='imagem',
            name='show_on_report',
            field=models.BooleanField(default=False),
        ),
    ]
