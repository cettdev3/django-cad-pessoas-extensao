# Generated by Django 4.2.2 on 2023-07-05 12:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sistema', '0137_escola_id_siga'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ensino',
            name='observacao',
            field=models.CharField(max_length=1500, null=True),
        ),
    ]
