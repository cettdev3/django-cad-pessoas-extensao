# Generated by Django 4.1.5 on 2023-01-25 13:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('sistema', '0052_tipoatividade'),
    ]

    operations = [
        migrations.CreateModel(
            name='Atividade',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('descricao', models.CharField(blank=True, max_length=300, null=True)),
                ('status', models.CharField(blank=True, max_length=50, null=True)),
                ('logradouro', models.CharField(blank=True, max_length=100, null=True)),
                ('bairro', models.CharField(blank=True, max_length=100, null=True)),
                ('cep', models.CharField(blank=True, max_length=20, null=True)),
                ('complemento', models.CharField(blank=True, max_length=250, null=True)),
                ('acao', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='sistema.acao')),
                ('cidade', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='sistema.cidade')),
                ('responsavel', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='sistema.membroexecucao')),
                ('tipoAtividade', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='sistema.tipoatividade')),
            ],
            options={
                'db_table': 'atividades',
            },
        ),
    ]
