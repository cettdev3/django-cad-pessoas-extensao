# Generated by Django 4.2.5 on 2023-09-13 16:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('sistema', '0173_transfer_role_to_role_model'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='membroexecucao',
            name='role',
        ),
    ]
