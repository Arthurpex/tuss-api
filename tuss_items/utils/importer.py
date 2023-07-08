import re

import pandas as pd
from datetime import datetime

import pytz
from django.db import transaction
from tuss_items.models import (
    DiariaTaxa,
    Medicamento,
    Procedimento,
    Material,
    TermoTuss,
    DemaisTerminologia, UnidadeFederacao, UnidadeMedida, ModeloRemuneracao, TipoDocumento, TabelasDominio, FormaEnvio,
)


def parse_date(date_string, format="%Y-%m-%d", timezone="UTC"):
    if (
        pd.isnull(date_string)
        or not isinstance(date_string, str)
        or len(date_string) < 8
    ):
        return None

    # Extract only the date portion using regex
    match = re.match(r"(\d{4}-\d{2}-\d{2})", date_string)
    if match:
        date_string = match.group(1)
    else:
        return None

    naive_dt = datetime.strptime(date_string, format)

    # Attach timezone information to the datetime object
    tz = pytz.timezone(timezone)
    aware_dt = tz.localize(naive_dt)

    return aware_dt


def import_large_csv2(csv_file_path, model_type, batch_size=1000):
    model_config = {
        "medicamento": {
            "model": TermoTuss,
            "fields": [
                ("codigo_tuss", "Código do Termo"),
                ("termo", "Termo"),
                ("tabela", "tabela"),
                ("dt_inicio_vigencia", "Data de início de vigência"),
                ("dt_fim_vigencia", "Data de fim de vigência"),
                ("dt_implantacao", "Data de fim de implantação"),
            ],
        },
        #
        # 'material': {
        #     'model': Material,
        #     'fields': [
        #         ('codigo_tuss', 'Código do Termo'),
        #         ('termo', 'Termo'),
        #         ('dt_inicio_vigencia', 'Data de início de vigência'),
        #         ('dt_fim_vigencia', 'Data de fim de vigência'),
        #         ('dt_implantacao', 'Data de fim de implantação'),
        #         ('codigo_anvisa', 'Registro Anvisa'),
        #         ('tabela', "tabela"),
        #     ]
        # },
        # 'procedimento': {
        #     'model': Procedimento,
        #     'fields': [
        #         ('descricao_detalhada', 'Descrição Detalhada'),
        #         ('codigo_tuss', 'Código do Termo'),
        #         ('termo', 'Termo'),
        #         ('dt_inicio_vigencia', 'Data de início de vigência'),
        #         ('dt_fim_vigencia', 'Data de fim de vigência'),
        #         ('dt_implantacao', 'Data de fim de implantação'),
        #         ('tabela', "tabela"),
        #     ]
        # },
        # 'demaisterminologia': {
        #     'model': DemaisTerminologia,
        #     'fields': [
        #         ('codigo_tuss', 'Código do Termo'),
        #         ('termo', 'Termo'),
        #         ('dt_inicio_vigencia', 'Data de início de vigência'),
        #         ('dt_fim_vigencia', 'Data de fim de vigência'),
        #         ('dt_implantacao', 'Data de fim de implantação'),
        #         ('tabela', "tabela"),
        #     ]
        # },
        # 'tabela59': {
        #     'model': Tabela59,
        #     'fields': [
        #         ('sigla', 'Sigla'),
        #         ('codigo_tuss', 'Código do Termo'),
        #         ('termo', 'Termo'),
        #         ('dt_inicio_vigencia', 'Data de início de vigência'),
        #         ('dt_fim_vigencia', 'Data de fim de vigência'),
        #         ('dt_implantacao', 'Data de fim de implantação'),
        #         ('tabela', "tabela"),
        #     ]
        # },
        # 'tabela60': {
        #     'model': Tabela60,
        #     'fields': [
        #         ('descricao_detalhada', 'Descrição Detalhada'),
        #         ('codigo_tuss', 'Código do Termo'),
        #         ('termo', 'Termo'),
        #         ('dt_inicio_vigencia', 'Data de início de vigência'),
        #         ('dt_fim_vigencia', 'Data de fim de vigência'),
        #         ('dt_implantacao', 'Data de fim de implantação'),
        #         ('tabela', "tabela"),
        #     ]
        # },
        # 'tabela79': {
        #     'model': Tabela79,
        #     'fields': [
        #         ('descricao_detalhada', 'Descrição Detalhada'),
        #         ('codigo_tuss', 'Código do Termo'),
        #         ('termo', 'Termo'),
        #         ('dt_inicio_vigencia', 'Data de início de vigência'),
        #         ('dt_fim_vigencia', 'Data de fim de vigência'),
        #         ('dt_implantacao', 'Data de fim de implantação'),
        #         ('tabela', "tabela"),
        #     ]
        # },
        # 'tabela81': {
        #     'model': Tabela81,
        #     'fields': [
        #         ('requer_assinatura', 'Requer assinatura digital na mensagem de envio'),
        #         ('codigo_tuss', 'Código do Termo'),
        #         ('termo', 'Termo'),
        #         ('dt_inicio_vigencia', 'Data de início de vigência'),
        #         ('dt_fim_vigencia', 'Data de fim de vigência'),
        #         ('dt_implantacao', 'Data de fim de implantação'),
        #         ('tabela', "tabela"),
        #     ]
        # },
        # 'tabela63': {
        #     'model': Tabela63,
        #     'fields': [
        #         ('codigo', 'Código'),
        #         ('grupo', 'Grupo'),
        #         ('dt_inicio_vigencia', 'Data de início de vigência'),
        #         ('dt_fim_vigencia', 'Data de fim de vigência'),
        #         ('dt_implantacao', 'Data de fim de implantação'),
        #         ('tabela', "tabela"),
        #     ]
        # },
        # 'tabela64': {
        #     'model': Tabela64,
        #     'fields': [
        #         ('terminologia', 'Terminologia'),
        #         ('codigo_do_grupo', 'Código do grupo'),
        #         ('forma_de_envio', 'Forma de envio'),
        #         ('descricao_do_grupo', 'Descrição do grupo'),
        #         ('codigo_tuss', 'Código TUSS'),
        #         ('dt_inicio_vigencia', 'Data de início de vigência'),
        #         ('dt_fim_vigencia', 'Data de fim de vigência'),
        #         ('dt_implantacao', 'Data de fim de implantação'),
        #         ('tabela', "tabela"),
        #     ]
        # },
        # 'tabela87': {
        #     'model': Tabela87,
        #     'fields': [
        #         ('codigo_tabela', 'Código da Tabela'),
        #         ('descricao', 'Descrição'),
        #         ('dt_inicio_vigencia', 'Data de início de vigência'),
        #         ('dt_fim_vigencia', 'Data de fim de vigência'),
        #         ('dt_implantacao', 'Data de fim de implantação'),
        #     ]
        # },
    }

    if model_type in model_config:
        config = model_config[model_type]

        model_class = config["model"]

        fields = config["fields"]

        csv_chunks = pd.read_csv(csv_file_path, chunksize=batch_size)

        for chunk in csv_chunks:
            records = chunk.to_dict("records")
            termo_tuss_list = []  # A new list for TermoTuss objects

            for record in records:
                termo_tuss = TermoTuss()  # Create an instance of TermoTuss

                for field, csv_field in fields:
                    print(f" ->>>>> field: {field} from {csv_file_path}")

                    value = record.get(csv_field)

                    if field == "codigo_tuss":
                        termo_tuss.codigo_tuss = str(value)

                    if "dt" in field:
                        try:
                            value = parse_date(value)
                        except ValueError:
                            value = parse_date(value, format="%d/%m/%Y")

                        if field == "dt_inicio_vigencia":
                            termo_tuss.dt_inicio_vigencia = value
                        elif field == "dt_fim_vigencia":
                            termo_tuss.dt_fim_vigencia = value
                        elif field == "dt_implantacao":
                            termo_tuss.dt_implantacao = value

                    if field == "tabela":
                        termo_tuss.tabela = value

                    if field == "termo":
                        termo_tuss.termo = value

                termo_tuss_list.append(
                    termo_tuss
                )  # Append the TermoTuss instance to the list

            with transaction.atomic():
                TermoTuss.objects.bulk_create(
                    termo_tuss_list
                )  # Create TermoTuss objects


def import_large_csv(csv_file_path, model_type, batch_size=1000):
    main_model_config = {
        "model": TermoTuss,
        "fields": [
            ("codigo_tuss", "Código do Termo"),
            ("termo", "Termo"),
            ("tabela", "tabela"),
            ("dt_inicio_vigencia", "Data de início de vigência"),
            ("dt_fim_vigencia", "Data de fim de vigência"),
            ("dt_implantacao", "Data de fim de implantação"),
        ],
    }

    model_config = {
        # 'medicamento': {
        #     'model': Medicamento,
        #     'fields': [
        #         ('codigo_anvisa', 'REGISTRO ANVISA'),
        #         ('apresentacao', 'Apresentação'),
        #         ('laboratorio', 'Laboratório'),
        #     ],
        # },
        # 'diariataxa': {
        #     'model': DiariaTaxa,
        #     'fields': [
        #         ('descricao_detalhada', 'Descrição Detalhada do Termo'),
        #     ]
        # },
        # 'material': {
        #     'model': Material,
        #     'fields': [
        #         ('codigo_anvisa', 'Registro Anvisa'),
        #         ('modelo', 'Modelo'),
        #         ('fabricante', 'Fabricante'),
        #         ('classe_risco', 'Classe de Risco'),
        #         ('nome_tecnico', 'NOME TÉCNICO'),
        #     ]
        # },
        # "procedimento": {
        #     "model": Procedimento,
        #     "fields": [
        #         ("descricao_detalhada", "Descrição Detalhada"),
        #     ],
        # },
        # 'demaisterminologia': {
        #     'model': DemaisTerminologia,
        #     'fields': [
        #     ]
        # },
        'unidadefederacao': {
            'model': UnidadeFederacao,
            'fields': [
                ('sigla', 'Sigla'),
            ]
        },
        'unidademedida': {
            'model': UnidadeMedida,
            'fields': [
                ('descricao_detalhada', 'Descrição Detalhada'),
            ]
        },
        'modeloremuneracao': {
            'model': ModeloRemuneracao,
            'fields': [
                ('descricao_detalhada', 'Descrição Detalhada'),
            ]
        },
        # 'tabela81': {
        #     'model': TipoDocumento,
        #     'fields': [
        #         ('requer_assinatura', 'Requer assinatura digital na mensagem de envio'),
        #     ]
        # },
    }

    if model_type not in model_config:
        if model_type in ["tabela87", "tabela64", "tabela63"]:
            # import_large_csv_special(csv_file_path, model_type, batch_size=batch_size)
            return

        print("Invalid model type: ", model_type)
        return

    print("Importing: ", model_type)
    specific_config = model_config[model_type]
    main_model = main_model_config["model"]
    main_fields = main_model_config["fields"]
    specific_model = specific_config["model"]
    specific_fields = specific_config["fields"]

    csv_chunks = pd.read_csv(csv_file_path, chunksize=batch_size)

    for chunk in csv_chunks:
        records = chunk.to_dict("records")
        main_model_list = []  # A new list for TermoTuss objects
        specific_model_list = []  # A new list for specific model objects

        for record in records:
            main_model_instance = main_model()  # Create an instance of the main model
            specific_model_instance = (
                specific_model()
            )  # Create an instance of the specific model

            for field, csv_field in main_fields:
                print(" ->>>>> field: ", field, " from ", csv_file_path)
                value = record.get(csv_field)

                if field == "codigo_tuss":
                    try:
                        # try to convert to int and catches exeception
                        value = int(value)
                    except TypeError:
                        value = str(value)
                    except ValueError:
                        value = str(value)
                    main_model_instance.codigo_tuss = str(value)
                elif "dt" in field:
                    try:
                        value = parse_date(value)
                    except ValueError:
                        value = parse_date(value, format="%d/%m/%Y")
                setattr(main_model_instance, field, value)

            main_model_list.append(
                main_model_instance
            )  # Append the main model instance to the list

            for field, csv_field in specific_fields:
                value = record.get(csv_field)
                setattr(specific_model_instance, field, value)

            specific_model_instance.termo_tuss = main_model_instance
            specific_model_list.append(
                specific_model_instance
            )  # Append the specific model instance to the list

        with transaction.atomic():
            main_model.objects.bulk_create(main_model_list)  # Create main model objects
            specific_model.objects.bulk_create(
                specific_model_list
            )  # Create specific model objects


def import_large_csv_special(csv_file_path, model_type, batch_size=1000):
    model_config = {
        "tabela63": {
            "model": Tabela63,
            "fields": [
                ("codigo", "Código"),
                ("grupo", "Grupo"),
                ("dt_inicio_vigencia", "Data de início de vigência"),
                ("dt_fim_vigencia", "Data de fim de vigência"),
                ("dt_implantacao", "Data de fim de implantação"),
                ("tabela", "tabela"),
            ],
        },
        "tabela64": {
            "model": FormaEnvio,
            "fields": [
                ("terminologia", "Terminologia"),
                ("codigo_do_grupo", "Código do grupo"),
                ("forma_de_envio", "Forma de envio"),
                ("codigo_tuss", "Código TUSS"),
                # ('descricao_do_grupo', 'Descrição do grupo'),
                # ('dt_inicio_vigencia', 'Data de início de vigência'),
                # ('dt_fim_vigencia', 'Data de fim de vigência'),
                # ('dt_implantacao', 'Data de fim de implantação'),
                # ('tabela', "tabela"),
            ],
        },
        "tabela87": {
            "model": TabelasDominio,
            "fields": [
                ("codigo_tabela", "Código da Tabela"),
                ("descricao", "Descrição"),
                ("dt_inicio_vigencia", "Data de início de vigência"),
                ("dt_fim_vigencia", "Data de fim de vigência"),
                ("dt_implantacao", "Data de fim de implantação"),
            ],
        },
    }

    if model_type not in model_config:
        return

    print("Importing special file: ", model_type)

    specific_config = model_config[model_type]
    specific_model = specific_config["model"]
    specific_fields = specific_config["fields"]

    csv_chunks = pd.read_csv(csv_file_path, chunksize=batch_size)

    for chunk in csv_chunks:
        records = chunk.to_dict("records")
        specific_model_list = []  # A new list for specific model objects

        for record in records:
            specific_model_instance = (
                specific_model()
            )  # Create an instance of the specific model

            for field, csv_field in specific_fields:
                value = record.get(csv_field)

                if "codigo_do_grupo" in field:
                    if pd.isna(value) or value == " ":
                        value = None

                if "dt" in field:
                    try:
                        value = parse_date(value)
                    except ValueError:
                        value = parse_date(value, format="%d/%m/%Y")

                setattr(specific_model_instance, field, value)

            specific_model_list.append(
                specific_model_instance
            )  # Append the specific model instance to the list

        with transaction.atomic():
            specific_model.objects.bulk_create(specific_model_list)
