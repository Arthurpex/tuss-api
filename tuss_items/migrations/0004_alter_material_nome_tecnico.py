# Generated by Django 4.1.2 on 2023-05-31 03:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tuss_items', '0003_alter_material_fabricante_alter_material_modelo_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='material',
            name='nome_tecnico',
            field=models.TextField(max_length=256),
        ),
    ]