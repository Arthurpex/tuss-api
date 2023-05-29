import re

import pandas as pd
from datetime import datetime

import pytz
from django.db import transaction
from tuss_items.models import DiariaTaxa, Medicamento, Procedimento, Material, DemaisTerminologia, Tabela59, Tabela60, \
    Tabela79, Tabela81, Tabela63, Tabela64, Tabela87


# def parse_date(date_string, format='%Y-%m-%d'):
#     if pd.isnull(date_string) or not isinstance(date_string, str) or len(date_string) < 8:
#         return None
#     return datetime.strptime(date_string, format)

def parse_date(date_string, format='%Y-%m-%d', timezone='UTC'):
    if pd.isnull(date_string) or not isinstance(date_string, str) or len(date_string) < 8:
        return None

    # Extract only the date portion using regex
    match = re.match(r'(\d{4}-\d{2}-\d{2})', date_string)
    if match:
        date_string = match.group(1)
    else:
        return None

    naive_dt = datetime.strptime(date_string, format)

    # Attach timezone information to the datetime object
    tz = pytz.timezone(timezone)
    aware_dt = tz.localize(naive_dt)

    return aware_dt


#
# def import_large_csv_diarias(csv_file_path, batch_size=1000):
#     # Define a function to parse date strings
#
#     # Read CSV in chunks using pandas
#     csv_chunks = pd.read_csv(csv_file_path, chunksize=batch_size)
#
#     for chunk in csv_chunks:
#         # Convert the pandas DataFrame chunk to a list of dictionaries
#         records = chunk.to_dict('records')
#
#         # Create a list of DiariasTaxas instances
#         diarias_taxas_list = [
#             DiariaTaxa(
#                 descricao_detalhada=record['Descrição Detalhada do Termo'],
#                 codigo_tuss=record['Código do Termo'],
#                 termo=record['Termo'],
#                 dt_inicio_vigencia=parse_date(record['Data de início de vigência']),
#                 dt_fim_vigencia=parse_date(record['Data de fim de vigência']),
#                 dt_implantacao=parse_date(record['Data de fim de implantação'])
#             )
#             for record in records
#         ]
#
#         # Use Django's bulk_create to insert records in batches
#         with transaction.atomic():
#             DiariaTaxa.objects.bulk_create(diarias_taxas_list)
#
#
# def import_large_csv_medicamento(csv_file_path, batch_size=1000):
#     # Define a function to parse date strings
#     def parse_date(date_string):
#         if pd.isnull(date_string):
#             return None
#         return datetime.strptime(date_string, '%Y-%m-%d')
#
#     # Read CSV in chunks using pandas
#     csv_chunks = pd.read_csv(csv_file_path, chunksize=batch_size)
#
#     for chunk in csv_chunks:
#         # Convert the pandas DataFrame chunk to a list of dictionaries
#         records = chunk.to_dict('records')
#
#         objects_list = [
#             Medicamento(
#                 codigo_tuss=int(record.get('Código do Termo')),
#                 termo=record.get('Termo'),
#                 apresentacao=record.get('Apresentação'),
#                 laboratorio=record.get('Laboratório'),
#                 dt_inicio_vigencia=parse_date(record.get('Data de início de vigência')),
#                 dt_fim_vigencia=parse_date(record.get('Data de fim de vigência')),
#                 dt_implantacao=parse_date(record.get('Data de fim de implantação')),
#                 codigo_anvisa=0 if type(record.get('REGISTRO ANVISA')) is not int else record.get('REGISTRO ANVISA')
#             )
#             for record in records
#         ]
#
#         # Use Django's bulk_create to insert records in batches
#         with transaction.atomic():
#             Medicamento.objects.bulk_create(objects_list)
#
#
# def import_large_csv_procedimento(csv_file_path, batch_size=1000):
#     # Define a function to parse date strings
#     def parse_date(date_string):
#         if pd.isnull(date_string):
#             return None
#         return datetime.strptime(date_string, '%Y-%m-%d')
#
#     # Read CSV in chunks using pandas
#     csv_chunks = pd.read_csv(csv_file_path, chunksize=batch_size)
#
#     for chunk in csv_chunks:
#         # Convert the pandas DataFrame chunk to a list of dictionaries
#         records = chunk.to_dict('records')
#
#         objects_list = [
#             Procedimento(
#                 descricao_detalhada=record['Descrição Detalhada'],
#                 codigo_tuss=record['Código do Termo'],
#                 termo=record['Termo'],
#                 dt_inicio_vigencia=parse_date(record['Data de início de vigência']),
#                 dt_fim_vigencia=parse_date(record['Data de fim de vigência']),
#                 dt_implantacao=parse_date(record['Data de fim de implantação'])
#             )
#
#             for record in records
#         ]
#
#         # Use Django's bulk_create to insert records in batches
#         with transaction.atomic():
#             Procedimento.objects.bulk_create(objects_list)
#
#
# def import_large_csv_material(csv_file_path, batch_size=1000):
#     # Define a function to parse date strings
#     def parse_date(date_string):
#         if pd.isnull(date_string):
#             return None
#         return datetime.strptime(date_string, '%Y-%m-%d')
#
#     # Read CSV in chunks using pandas
#     csv_chunks = pd.read_csv(csv_file_path, chunksize=batch_size)
#
#     for chunk in csv_chunks:
#         # Convert the pandas DataFrame chunk to a list of dictionaries
#         records = chunk.to_dict('records')
#
#         objects_list = [
#             Material(
#                 modelo=record["Modelo"],
#                 fabricante=record["Fabricante"],
#                 codigo_anvisa=record["Registro Anvisa"],
#                 classe_risco=record['NOME TÉCNICO'],
#                 nome_tecnico=record['Classe de Risco'],
#                 codigo_tuss=record['Código do Termo'],
#                 termo=record['Termo'],
#                 dt_inicio_vigencia=parse_date(record['Data de início de vigência']),
#                 dt_fim_vigencia=parse_date(record['Data de fim de vigência']),
#                 dt_implantacao=parse_date(record['Data de fim de implantação'])
#
#             )
#             for record in records
#         ]
#
#         # Use Django's bulk_create to insert records in batches
#         with transaction.atomic():
#             Material.objects.bulk_create(objects_list)
#


def import_large_csv(csv_file_path, model_type, batch_size=1000):
    model_config = {
        'diariataxa': {
            'model': DiariaTaxa,
            'fields': [
                ('descricao_detalhada', 'Descrição Detalhada do Termo'),
                ('codigo_tuss', 'Código do Termo'),
                ('termo', 'Termo'),
                ('dt_inicio_vigencia', 'Data de início de vigência'),
                ('dt_fim_vigencia', 'Data de fim de vigência'),
                ('dt_implantacao', 'Data de fim de implantação'),
                ('tabela', "tabela"),
            ]
        },
        'medicamento': {
            'model': Medicamento,
            'fields': [
                ('codigo_tuss', 'Código do Termo'),
                ('termo', 'Termo'),
                ('apresentacao', 'Apresentação'),
                ('laboratorio', 'Laboratório'),
                ('dt_inicio_vigencia', 'Data de início de vigência'),
                ('dt_fim_vigencia', 'Data de fim de vigência'),
                ('dt_implantacao', 'Data de fim de implantação'),
                ('codigo_anvisa', 'REGISTRO ANVISA'),
                ('tabela', "tabela"),

            ]
        },
        'material': {
            'model': Material,
            'fields': [
                ('codigo_tuss', 'Código do Termo'),
                ('termo', 'Termo'),
                ('dt_inicio_vigencia', 'Data de início de vigência'),
                ('dt_fim_vigencia', 'Data de fim de vigência'),
                ('dt_implantacao', 'Data de fim de implantação'),
                ('codigo_anvisa', 'Registro Anvisa'),
                ('tabela', "tabela"),
            ]
        },
        'procedimento': {
            'model': Procedimento,
            'fields': [
                ('descricao_detalhada', 'Descrição Detalhada'),
                ('codigo_tuss', 'Código do Termo'),
                ('termo', 'Termo'),
                ('dt_inicio_vigencia', 'Data de início de vigência'),
                ('dt_fim_vigencia', 'Data de fim de vigência'),
                ('dt_implantacao', 'Data de fim de implantação'),
                ('tabela', "tabela"),
            ]
        },
        'demaisterminologia': {
            'model': DemaisTerminologia,
            'fields': [
                ('codigo_tuss', 'Código do Termo'),
                ('termo', 'Termo'),
                ('dt_inicio_vigencia', 'Data de início de vigência'),
                ('dt_fim_vigencia', 'Data de fim de vigência'),
                ('dt_implantacao', 'Data de fim de implantação'),
                ('tabela', "tabela"),
            ]
        },
        'tabela59': {
            'model': Tabela59,
            'fields': [
                ('sigla', 'Sigla'),
                ('codigo_tuss', 'Código do Termo'),
                ('termo', 'Termo'),
                ('dt_inicio_vigencia', 'Data de início de vigência'),
                ('dt_fim_vigencia', 'Data de fim de vigência'),
                ('dt_implantacao', 'Data de fim de implantação'),
                ('tabela', "tabela"),
            ]
        },
        'tabela60': {
            'model': Tabela60,
            'fields': [
                ('descricao_detalhada', 'Descrição Detalhada'),
                ('codigo_tuss', 'Código do Termo'),
                ('termo', 'Termo'),
                ('dt_inicio_vigencia', 'Data de início de vigência'),
                ('dt_fim_vigencia', 'Data de fim de vigência'),
                ('dt_implantacao', 'Data de fim de implantação'),
                ('tabela', "tabela"),
            ]
        },
        'tabela79': {
            'model': Tabela79,
            'fields': [
                ('descricao_detalhada', 'Descrição Detalhada'),
                ('codigo_tuss', 'Código do Termo'),
                ('termo', 'Termo'),
                ('dt_inicio_vigencia', 'Data de início de vigência'),
                ('dt_fim_vigencia', 'Data de fim de vigência'),
                ('dt_implantacao', 'Data de fim de implantação'),
                ('tabela', "tabela"),
            ]
        },
        'tabela81': {
            'model': Tabela81,
            'fields': [
                ('requer_assinatura', 'Requer assinatura digital na mensagem de envio'),
                ('codigo_tuss', 'Código do Termo'),
                ('termo', 'Termo'),
                ('dt_inicio_vigencia', 'Data de início de vigência'),
                ('dt_fim_vigencia', 'Data de fim de vigência'),
                ('dt_implantacao', 'Data de fim de implantação'),
                ('tabela', "tabela"),
            ]
        },
        'tabela63': {
            'model': Tabela63,
            'fields': [
                ('codigo', 'Código'),
                ('grupo', 'Grupo'),
                ('dt_inicio_vigencia', 'Data de início de vigência'),
                ('dt_fim_vigencia', 'Data de fim de vigência'),
                ('dt_implantacao', 'Data de fim de implantação'),
                ('tabela', "tabela"),
            ]
        },
        'tabela64': {
            'model': Tabela64,
            'fields': [
                ('terminologia', 'Terminologia'),
                ('codigo_do_grupo', 'Código do grupo'),
                ('forma_de_envio', 'Forma de envio'),
                ('descricao_do_grupo', 'Descrição do grupo'),
                ('codigo_tuss', 'Código TUSS'),
                ('dt_inicio_vigencia', 'Data de início de vigência'),
                ('dt_fim_vigencia', 'Data de fim de vigência'),
                ('dt_implantacao', 'Data de fim de implantação'),
                ('tabela', "tabela"),
            ]
        },
        'tabela87': {
            'model': Tabela87,
            'fields': [
                ('codigo_tabela', 'Código da Tabela'),
                ('descricao', 'Descrição'),
                ('dt_inicio_vigencia', 'Data de início de vigência'),
                ('dt_fim_vigencia', 'Data de fim de vigência'),
                ('dt_implantacao', 'Data de fim de implantação'),
            ]
        },
    }

    if model_type in model_config:
        config = model_config[model_type]
        model_class = config['model']
        fields = config['fields']

        csv_chunks = pd.read_csv(csv_file_path, chunksize=batch_size)

        for chunk in csv_chunks:
            records = chunk.to_dict('records')
            objects_list = []

            for record in records:
                obj = model_class()
                for field, csv_field in fields:
                    print(f" ->>>>> field: {field} from {csv_file_path}")

                    value = record.get(csv_field)

                    if field == 'codigo_tuss':
                        if isinstance(value, float):
                            value = str(int(value))  # Convert float to integer, then to string
                        elif isinstance(value, int):
                            value = str(value)  # Convert integer to string

                        if not value.isdigit():
                            value = ''.join(str(ord(c)) for c in value)

                    if 'dt' in field:
                        try:
                            value = parse_date(value)
                        except ValueError:
                            # value = parse_date(value, format="%d-%m-%Y")
                            value = parse_date(value, format="%d/%m/%Y")

                    if field == 'codigo_anvisa' and type(value) is not int:
                        value = 0
                    if field == 'codigo_do_grupo' and type(value) is not int:
                        value = 0

                    setattr(obj, field, value)

                objects_list.append(obj)

            with transaction.atomic():
                model_class.objects.bulk_create(objects_list)
