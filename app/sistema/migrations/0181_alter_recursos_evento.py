# Generated by Django 4.2.5 on 2023-09-15 04:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('sistema', '0180_recursos_evento'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recursos',
            name='evento',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='recursos', to='sistema.dpevento'),
        ),
    ]
