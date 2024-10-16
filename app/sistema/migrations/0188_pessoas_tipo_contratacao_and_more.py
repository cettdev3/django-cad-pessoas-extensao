# Generated by Django 4.2.5 on 2023-09-30 15:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sistema', '0187_alocacao_numero_matricula'),
    ]

    operations = [
        migrations.AddField(
            model_name='pessoas',
            name='tipo_contratacao',
            field=models.CharField(blank=True, choices=[('efetivo', 'Efetivo'), ('rpa', 'RPA'), ('outro', 'Outro')], max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='propostaprojeto',
            name='status',
            field=models.CharField(choices=[('rascunho', 'Rascunho'), ('em_analise', 'Em análise'), ('em_analise_direcao', 'Em análise pela direção'), ('em_analise_cett', 'Em análise pelo CETT'), ('devolvida', 'Devolvida'), ('aprovada', 'Aprovada'), ('reprovada', 'Reprovada'), ('cancelada', 'Cancelada'), ('solicitar_mudanca', 'Mudança solicitada'), ('devolvida_apos_aprovacao', 'Devolvida após aprovação')], default='em_analise', max_length=255),
        ),
    ]
