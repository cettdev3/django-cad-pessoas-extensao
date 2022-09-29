# Generated by Django 4.1.1 on 2022-09-26 20:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sistema', '0002_alter_pessoas_id'),
    ]

    operations = [
        migrations.CreateModel(
            name='Avaliacao',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('nome', models.CharField(max_length=100)),
                ('endereco', models.CharField(max_length=100)),
                ('curso', models.CharField(max_length=100)),
                ('qtd_salas', models.CharField(max_length=100)),
                ('capacidade', models.CharField(max_length=100)),
                ('qtd_cadeiras', models.CharField(max_length=100)),
                ('qtd_tomadas', models.CharField(max_length=100)),
                ('qtd_janelas', models.CharField(max_length=100)),
                ('tipo_climatizacao', models.CharField(max_length=100)),
                ('qualidade_iluminacao', models.CharField(max_length=100)),
                ('turnos_disponiveis', models.CharField(max_length=100)),
                ('qtd_banheiros_masculino', models.CharField(max_length=100)),
                ('qtd_banheiros_feminino', models.CharField(max_length=100)),
                ('rede_eletrica', models.CharField(max_length=100)),
                ('qualidade_bebedouro', models.CharField(max_length=100)),
                ('acessibilidade', models.CharField(max_length=100)),
                ('internet', models.CharField(max_length=100)),
                ('data_show', models.CharField(max_length=100)),
                ('limpeza', models.CharField(max_length=100)),
                ('link_imagens', models.CharField(max_length=100)),
                ('parecer', models.CharField(max_length=100)),
                ('possui_cozinha', models.CharField(max_length=100)),
                ('capacidade_cozinha', models.CharField(max_length=100)),
                ('qtd_tomadas_cozinha', models.CharField(max_length=100)),
                ('funcionalidade_fogao', models.CharField(max_length=100)),
                ('refrigeracao', models.CharField(max_length=100)),
                ('gas', models.CharField(max_length=100)),
                ('bancadas_mesas', models.CharField(max_length=100)),
                ('capacidade_fornos', models.CharField(max_length=100)),
                ('qtd_fornos', models.CharField(max_length=100)),
                ('ventilacao_cozinha', models.CharField(max_length=100)),
                ('torneiras_funcionam', models.CharField(max_length=100)),
                ('area_complementar', models.CharField(max_length=100)),
                ('observacao_cozinha', models.CharField(max_length=100)),
                ('laboratorio_informatica', models.CharField(max_length=100)),
                ('qtd_computadores', models.CharField(max_length=100)),
                ('cabeamento_internet', models.CharField(max_length=100)),
                ('qtd_computadores_wifi', models.CharField(max_length=100)),
                ('obs_informatica', models.CharField(max_length=100)),
                ('lavatorio', models.CharField(max_length=100)),
                ('qtd_lavatorio_sb', models.CharField(max_length=100)),
                ('cadeiras_de_sb', models.CharField(max_length=100)),
                ('qtd_cadeiras_sb', models.CharField(max_length=100)),
                ('cidade', models.CharField(max_length=100)),
            ],
            options={
                'db_table': 'avaliacoes',
            },
        ),
    ]
