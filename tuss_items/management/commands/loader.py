import os
import re
import time

from django.conf import settings
from django.core.management import BaseCommand

from tuss_items.utils.importer import import_large_csv, import_large_csv_special
from tuss_items.models import (
    Material,
    DiariaTaxa,
    Procedimento,
    Medicamento,
    DemaisTerminologia,
    UnidadeFederacao,
    UnidadeMedida,
    ModeloRemuneracao,
    GrupoEnvio,
    TipoDocumento,
    FormaEnvio,
    TabelasDominio,
)


def get_file_to_model_dict() -> dict:
    file_names = os.listdir(settings.MEDIA_ROOT + "/tuss_csvs")

    file_to_model = {}

    for file_name in file_names:
        match = re.search(r"\btab (\d{2})\b", file_name.lower())

        if match:
            tab_number = int(match.group(1))

            if tab_number == 18:
                model = DiariaTaxa
            elif tab_number == 22:
                model = Procedimento
            elif tab_number == 59:
                model = UnidadeFederacao
            elif tab_number == 60:
                model = UnidadeMedida
            elif tab_number == 79:
                model = ModeloRemuneracao
            elif tab_number == 81:
                model = TipoDocumento
            elif tab_number == 63:
                model = GrupoEnvio
            elif tab_number == 64:
                model = FormaEnvio
            elif tab_number == 18:
                model = DiariaTaxa
            elif tab_number == 87:
                model = TabelasDominio
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
    help = "Load csv files into database"

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.SUCCESS("Loading TUSS files into database..."))

        # keep track of the time it took

        start_time = time.time()

        file_to_model_map = get_file_to_model_dict()

        for file_name, model in file_to_model_map.items():
            import_large_csv(
                settings.MEDIA_ROOT + "/tuss_csvs/" + file_name,
                model_type=model._meta.model_name,
            )
            # import_large_csv_special(settings.MEDIA_ROOT + "/tuss_csvs/" + file_name, model_type=model._meta.model_name)

        # print the time it took
        print("--- %s seconds ---" % (time.time() - start_time))

        self.stdout.write(self.style.SUCCESS("Files loaded successfully"))
