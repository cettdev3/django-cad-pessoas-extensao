# Generated by Django 4.2.1 on 2023-05-30 10:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sistema', '0125_alter_tipoatividade_nome'),
    ]

    operations = [
        migrations.AddField(
            model_name='ticket',
            name='from_export',
            field=models.BooleanField(default=False),
        ),
    ]
