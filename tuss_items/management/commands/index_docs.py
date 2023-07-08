import time

from django.core.management import BaseCommand
from django_elasticsearch_dsl import Index
from elasticsearch_dsl.connections import connections

from django.conf import settings

from tuss_items.documents import TermoTussDocument, ExtraFieldsDocument
from tuss_items.models import (
    Procedimento,
    DiariaTaxa,
    DemaisTerminologia,
    Material,
    Medicamento,
    TermoTuss,
    UnidadeFederacao,
    UnidadeMedida,
    ModeloRemuneracao,
    TipoDocumento,
)

connections.create_connection(**settings.ELASTICSEARCH_DSL["default"])


def try_parse_int(value):
    try:
        return int(value)
    except ValueError:
        return None
    except TypeError:
        return None


class Command(BaseCommand):
    def handle(self, *args, **options):
        # TermoTussDocument.init()

        # tabelas_not_demais = [18, 22, 59, 60, 79, 81, 63, 64, 87, 19, 20]
        #
        # demais_terminologias = TermoTuss.objects.exclude(tabela__in=tabelas_not_demais)
        #
        # diaria_taxas = TermoTuss.objects.filter(tabela=18)
        #
        # materiais = TermoTuss.objects.filter(tabela=19)
        #
        # procedimentos = TermoTuss.objects.filter(tabela=22)
        # medicamentos = TermoTuss.objects.filter(tabela=20)

        tres_tabela = TermoTuss.objects.filter(tabela__in=[59, 60, 79])

        # self.index_model(medicamentos, "Medicamento")
        # self.index_model(diaria_taxas, "DiariaTaxa")
        # self.index_model(procedimentos, "Procedimento")
        # self.index_model(demais_terminologias, "DemaisTerminologia")
        #
        # self.index_model(materiais, "Material")

    def index_model(self, queryset, label):
        TermoTussDocument.init()

        related_models = [
            Material,
            Medicamento,
            Procedimento,
            DiariaTaxa,
            DemaisTerminologia,
            UnidadeFederacao,
            UnidadeMedida,
            ModeloRemuneracao,
            TipoDocumento,
        ]

        start_time = time.time()

        for termo_tuss in queryset:
            print(f"Indexing: {termo_tuss.id} from {termo_tuss.tabela}", flush=True)

            termo_tuss_document = TermoTussDocument()

            termo_tuss_document.id = termo_tuss.id
            termo_tuss_document.codigo_tuss = try_parse_int(termo_tuss.codigo_tuss)
            termo_tuss_document.tabela = termo_tuss.tabela
            termo_tuss_document.termo = termo_tuss.termo
            termo_tuss_document.dt_inicio_vigencia = termo_tuss.dt_inicio_vigencia
            termo_tuss_document.dt_fim_vigencia = termo_tuss.dt_fim_vigencia
            termo_tuss_document.dt_implantacao = termo_tuss.dt_implantacao

            related_model = None

            # iterate over each related model
            for related_model_class in related_models:
                try:
                    related_model = related_model_class.objects.get(
                        termo_tuss=termo_tuss
                    )
                    break
                except related_model_class.DoesNotExist:
                    pass

            if related_model is not None:
                codigo_anvisa = try_parse_int(
                    getattr(related_model, "codigo_anvisa", None)
                )

                related_model_document = ExtraFieldsDocument(
                    modelo=getattr(related_model, "modelo", None),
                    fabricante=getattr(related_model, "fabricante", None),
                    codigo_anvisa=codigo_anvisa,
                    nome_tecnico=getattr(related_model, "nome_tecnico", None),
                    apresentacao=getattr(related_model, "apresentacao", None),
                    laboratorio=getattr(related_model, "laboratorio", None),
                    descricao_detalhada=getattr(
                        related_model, "descricao_detalhada", None
                    ),
                    sigla=getattr(related_model, "sigla", None),
                )

                termo_tuss_document.related_model = related_model_document
            termo_tuss_document.save()

        end_time = time.time()
        return end_time - start_time
