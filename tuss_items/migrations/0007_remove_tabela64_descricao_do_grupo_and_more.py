# Generated by Django 4.1.2 on 2023-06-03 04:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tuss_items', '0006_alter_material_classe_risco_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tabela64',
            name='descricao_do_grupo',
        ),
        migrations.RemoveField(
            model_name='tabela64',
            name='dt_fim_vigencia',
        ),
        migrations.RemoveField(
            model_name='tabela64',
            name='dt_implantacao',
        ),
        migrations.RemoveField(
            model_name='tabela64',
            name='dt_inicio_vigencia',
        ),
        migrations.RemoveField(
            model_name='tabela64',
            name='tabela',
        ),
    ]