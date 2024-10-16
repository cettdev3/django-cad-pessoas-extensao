# Generated by Django 4.1.5 on 2023-01-23 19:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sistema', '0051_alter_itinerario_table'),
    ]

    operations = [
        migrations.CreateModel(
            name='TipoAtividade',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('nome', models.CharField(max_length=50, null=True)),
                ('descricao', models.CharField(blank=True, max_length=250, null=True)),
                ('categoria', models.CharField(blank=True, max_length=50, null=True)),
            ],
            options={
                'db_table': 'tipos_atividades',
            },
        ),
    ]
