from django.db import migrations

def migrate_orcamentoitem_to_recursos(apps, schema_editor):
    OrcamentoItem = apps.get_model('sistema', 'OrcamentoItem')
    PropostaProjeto = apps.get_model('sistema', 'PropostaProjeto')
    Recursos = apps.get_model('sistema', 'Recursos')
    
    for orcamento_item in OrcamentoItem.objects.all():
        # Get related PropostaProjeto from Orcamento
        proposta_projeto = PropostaProjeto.objects.get(orcamento=orcamento_item.orcamento)

        # Create Recursos instance
        recursos_data = {
            "proposta_projeto": proposta_projeto,
            "nome": orcamento_item.descricao,
            "descricao": orcamento_item.descricao,
            "quantidade": orcamento_item.quantidade,
            "unidade": orcamento_item.unidade,
            "valor": orcamento_item.valor,
            "valor_total": orcamento_item.valor_total,
            "em_estoque": orcamento_item.em_estoque
        }

        # Only add evento if it exists for the PropostaProjeto
        has_evento = hasattr(proposta_projeto, 'evento')
        if has_evento:
            print("has evento")
            recursos_data["evento"] = proposta_projeto.evento
        else:
            print("does not have evento")
        Recursos.objects.create(**recursos_data)


class Migration(migrations.Migration):

    dependencies = [
        ('sistema', '0181_alter_recursos_evento'),
    ]

    operations = [
        migrations.RunPython(migrate_orcamentoitem_to_recursos),
    ]
