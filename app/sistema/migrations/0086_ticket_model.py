# Generated by Django 4.1.7 on 2023-04-04 18:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sistema', '0085_remove_alocacao_tipo'),
    ]

    operations = [
        migrations.AddField(
            model_name='ticket',
            name='model',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
