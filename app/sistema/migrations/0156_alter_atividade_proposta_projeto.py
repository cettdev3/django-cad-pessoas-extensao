# Generated by Django 4.2.3 on 2023-07-24 16:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('sistema', '0155_alter_membroexecucao_proposta_projeto'),
    ]

    operations = [
        migrations.AlterField(
            model_name='atividade',
            name='proposta_projeto',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='atividades', to='sistema.propostaprojeto'),
        ),
    ]
