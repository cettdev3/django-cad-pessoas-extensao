# Generated by Django 4.2.3 on 2023-07-27 16:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('sistema', '0161_propostaprojeto_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='propostaprojeto',
            name='escola',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='sistema.escola'),
        ),
        migrations.AlterField(
            model_name='propostaprojeto',
            name='status',
            field=models.CharField(choices=[('em_analise', 'Em análise'), ('devolvida', 'Devolvida'), ('aprovada', 'Aprovada'), ('reprovada', 'Reprovada'), ('cancelada', 'Cancelada')], default='em_analise', max_length=255),
        ),
    ]
