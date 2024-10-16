# Generated by Django 4.1.4 on 2022-12-16 12:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('sistema', '0042_acao_escola'),
    ]

    operations = [
        migrations.CreateModel(
            name='Ticket',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('tipo', models.CharField(max_length=100, null=True)),
                ('status', models.CharField(max_length=100, null=True)),
                ('id_protocolo', models.CharField(max_length=100, null=True)),
                ('meta', models.JSONField(null=True)),
                ('membro_execucao', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='sistema.membroexecucao')),
            ],
            options={
                'db_table': 'tickets',
            },
        ),
    ]
