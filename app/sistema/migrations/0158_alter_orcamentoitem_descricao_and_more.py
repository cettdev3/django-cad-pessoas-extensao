# Generated by Django 4.2.3 on 2023-07-26 02:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('sistema', '0157_membroexecucao_instituicao'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orcamentoitem',
            name='descricao',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='orcamentoitem',
            name='orcamento',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='items', to='sistema.orcamento'),
        ),
        migrations.AlterField(
            model_name='orcamentoitem',
            name='quantidade',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='orcamentoitem',
            name='tipo',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='orcamentoitem',
            name='unidade',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='orcamentoitem',
            name='valor',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=7, null=True),
        ),
        migrations.AlterField(
            model_name='orcamentoitem',
            name='valor_total',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=7, null=True),
        ),
    ]
