# Generated by Django 4.2.1 on 2023-06-02 16:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sistema', '0134_atividadecategoria_slug_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='atividadecategoria',
            name='id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
    ]
