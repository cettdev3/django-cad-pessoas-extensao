# Generated by Django 4.2.1 on 2023-05-31 13:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('sistema', '0127_ticket_rubrica'),
    ]

    operations = [
        migrations.AddField(
            model_name='ticket',
            name='departamento',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='sistema.departamento'),
        ),
    ]
