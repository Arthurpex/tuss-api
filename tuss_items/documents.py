from django_elasticsearch_dsl import Document
from django_elasticsearch_dsl.registries import registry
from elasticsearch_dsl import Text, Integer

from .models import Medicamento, Material, Procedimento, Tabela59, Tabela63, Tabela64, Tabela87, DemaisTerminologia, \
    DiariaTaxa, Tabela81, Tabela79, Tabela60

class MedicamentoDocument(Document):
    tabela = Integer()
    codigo_tuss = Text()
    termo = Text()
    apresentacao = Text()
    laboratorio = Text()
    codigo_anvisa = Text()
    # dt_inicio_vigencia = Date()
    # dt_fim_vigencia = Date()
    # dt_implantacao = Date()

    class Index:
        name = 'medicamento_index'

class MaterialDocument(Document):
    tabela = Integer()
    codigo_tuss = Text()
    termo = Text()
    modelo = Text()
    fabricante = Text()
    codigo_anvisa = Text()
    classe_risco = Text()
    nome_tecnico = Text()

    class Index:
        name = 'material_index'


# @registry.register_document
# class MedicamentoDocument(Document):
#     class Index:
#         name = 'medicamento_index'
#
#     class Django:
#         model = Medicamento
#         fields = [
#             'tabela',
#             'codigo_tuss',
#             'termo',
#             'apresentacao',
#             'laboratorio',
#             'codigo_anvisa',
#             # 'dt_inicio_vigencia',
#             # 'dt_fim_vigencia',
#             # 'dt_implantacao',
#         ]
#
#
# @registry.register_document
# class MaterialDocument(Document):
#     class Index:
#         name = 'material_index'
#         settings = {'number_of_shards': 1, 'number_of_replicas': 1}
#
#     class Django:
#         model = Material
#         fields = [
#             'tabela',
#             'codigo_tuss',
#             'termo',
#             'modelo',
#             'fabricante',
#             'codigo_anvisa',
#             'classe_risco',
#             'nome_tecnico',
#         ]
#
#
# @registry.register_document
# class ProcedimentoDocument(Document):
#     class Index:
#         name = 'procedimento_index'
#         settings = {'number_of_shards': 1, 'number_of_replicas': 1}
#
#     class Django:
#         model = Procedimento
#         fields = [
#             'tabela',
#             'codigo_tuss',
#             'termo',
#             'descricao_detalhada',
#         ]
#
#
# @registry.register_document
# class DiariaTaxaDocument(Document):
#     class Index:
#         name = 'diaria_taxa_index'
#         settings = {'number_of_shards': 1, 'number_of_replicas': 1}
#
#     class Django:
#         model = DiariaTaxa
#         fields = [
#             'tabela',
#             'codigo_tuss',
#             'termo',
#             'descricao_detalhada',
#         ]
#
#
# @registry.register_document
# class DemaisTerminologiaDocument(Document):
#     class Index:
#         name = 'demais_terminologia_index'
#         settings = {'number_of_shards': 1, 'number_of_replicas': 1}
#
#     class Django:
#         model = DemaisTerminologia
#         fields = [
#             'tabela',
#             'codigo_tuss',
#             'termo',
#         ]
#
#
# @registry.register_document
# class Tabela59Document(Document):
#     class Index:
#         name = 'tabela_59_index'
#         settings = {'number_of_shards': 1, 'number_of_replicas': 1}
#
#     class Django:
#         model = Tabela59
#         fields = [
#             'tabela',
#             'codigo_tuss',
#             'termo',
#             'sigla',
#         ]
#
#
# @registry.register_document
# class Tabela60Document(Document):
#     class Index:
#         name = 'tabela_60_index'
#         settings = {'number_of_shards': 1, 'number_of_replicas': 1}
#
#     class Django:
#         model = Tabela60
#         fields = [
#             'codigo_tuss',
#             'descricao_detalhada',
#             'termo',
#         ]
#
#
#
#
# @registry.register_document
# class Tabela63Document(Document):
#     class Index:
#         name = 'tabela_63_index'
#         settings = {'number_of_shards': 1, 'number_of_replicas': 1}
#
#     class Django:
#         model = Tabela63
#         fields = [
#             'tabela',
#             'codigo',
#             'grupo',
#         ]
#
#
# # @registry.register_document
# # class Tabela64Document(Document):
# #     class Index:
# #         name = 'tabela_64_index'
# #         settings = {'number_of_shards': 1, 'number_of_replicas': 1}
# #
# #     class Django:
# #         model = Tabela64
# #         fields = [
# #             'tabela',
# #             'codigo_tuss',
# #             'terminologia',
# #             'forma_de_envio',
# #             'codigo_do_grupo',
# #             'descricao_do_grupo',
# #         ]
#
# @registry.register_document
# class Tabela79Document(Document):
#     class Index:
#         name = 'tabela_79_index'
#         settings = {'number_of_shards': 1, 'number_of_replicas': 1}
#
#     class Django:
#         model = Tabela79
#         fields = [
#             'codigo_tuss',
#             'descricao_detalhada',
#             'termo',
#         ]
#
#
#
# @registry.register_document
# class Tabela81Document(Document):
#     class Index:
#         name = 'tabela_81_index'
#         settings = {'number_of_shards': 1, 'number_of_replicas': 1}
#
#     class Django:
#         model = Tabela81
#         fields = [
#             'codigo_tuss',
#             'requer_assinatura',
#             'termo',
#         ]
#
#
#
# @registry.register_document
# class Tabela87Document(Document):
#     class Index:
#         name = 'tabela_87_index'
#         settings = {'number_of_shards': 1, 'number_of_replicas': 1}
#
#     class Django:
#         model = Tabela87
#         fields = [
#             'codigo_tabela',
#             'descricao',
#         ]
