# Generated by Django 4.2.3 on 2023-07-21 19:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('sistema', '0149_atividade_proposta_projeto'),
    ]

    operations = [
        migrations.AddField(
            model_name='membroexecucao',
            name='proposta_projeto',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='sistema.propostaprojeto'),
        ),
    ]
