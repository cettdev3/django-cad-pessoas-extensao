# Generated by Django 4.1.5 on 2023-02-01 16:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sistema', '0062_atividade_evento'),
    ]

    operations = [
        migrations.CreateModel(
            name='Departamento',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('nome', models.CharField(max_length=100, null=True)),
            ],
            options={
                'db_table': 'departamentos',
            },
        ),
    ]
