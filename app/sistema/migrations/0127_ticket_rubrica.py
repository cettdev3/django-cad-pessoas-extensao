# Generated by Django 4.2.1 on 2023-05-30 11:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sistema', '0126_ticket_from_export'),
    ]

    operations = [
        migrations.AddField(
            model_name='ticket',
            name='rubrica',
            field=models.CharField(blank=True, max_length=250, null=True),
        ),
    ]
