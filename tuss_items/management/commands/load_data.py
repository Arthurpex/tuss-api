import os
import re
import shutil
from django.conf import settings
from django.core.management import BaseCommand

from tuss_items.utils.importer import import_large_csv
from tuss_items.models import Tabela59, DemaisTerminologia, Material, DiariaTaxa, Procedimento, Medicamento, Tabela64, \
    Tabela63, Tabela81, Tabela79, Tabela60, Tabela87

# Configuration object

def move_csv_files():
    root_dir = settings.MEDIA_ROOT
    output_folder = 'tuss_csvs'
    output_dir = os.path.join(root_dir, output_folder)

    # Create the output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)

    # Walk through the root directory and its subdirectories
    for subdir, _, files in os.walk(root_dir):
        for file in files:
            # Check if the file has a .csv extension
            if file.endswith('.csv'):
                file_path = os.path.join(subdir, file)
                # Move the file to the output directory
                shutil.move(file_path, os.path.join(output_dir, file))
                print(f"Moved {file_path} to {output_dir}")


def get_file_to_model_dict(file_names) -> dict:
    file_to_model = {}

    for file_name in file_names:
        match = re.search(r'\btab (\d{2})\b', file_name.lower())

        if match:
            tab_number = int(match.group(1))

            if tab_number == 18:
                model = DiariaTaxa
            elif tab_number == 22:
                model = Procedimento
            elif tab_number == 59:
                model = Tabela59
            elif tab_number == 60:
                model = Tabela60
            elif tab_number == 79:
                model = Tabela79
            elif tab_number == 81:
                model = Tabela81
            elif tab_number == 63:
                model = Tabela63
            elif tab_number == 64:
                model = Tabela64
            elif tab_number == 18:
                model = DiariaTaxa
            elif tab_number == 87:
                model = Tabela87
            else:
                model = DemaisTerminologia

            file_to_model[file_name] = model

        else:
            if "medicamento" in file_name.lower():
                model = Medicamento
            if "materiais e opme" in file_name.lower():
                model = Material

            file_to_model[file_name] = model

    return file_to_model


class Command(BaseCommand):
    help = 'Load csv files into database'

    def handle(self, *args, **kwargs):
        move_csv_files()

        files = os.listdir(settings.MEDIA_ROOT+"/tuss_csvs")

        file_to_model_map = get_file_to_model_dict(files)

        for file_name, model in file_to_model_map.items():
            import_large_csv(settings.MEDIA_ROOT + "/tuss_csvs/" + file_name, model_type=model._meta.model_name)
