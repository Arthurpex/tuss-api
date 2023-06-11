# from django.contrib import admin
# from import_export import resources
# from import_export.admin import ImportExportMixin
#
# from tuss_items.models import Medicamento, Procedimento, Material, DiariaTaxa, DemaisTerminologia
#
#
# class MedicamentoResource(resources.ModelResource):
#     class Meta:
#         model = Medicamento
#
# class ProcedimentoResource(resources.ModelResource):
#     class Meta:
#         model = Procedimento
#
# class MaterialResource(resources.ModelResource):
#     class Meta:
#         model = Material
#
# class DiariaTaxaResource(resources.ModelResource):
#     class Meta:
#         model = DiariaTaxa
#
# class DemaisTerminologiaResource(resources.ModelResource):
#     class Meta:
#         model = DemaisTerminologia
#
#
#
#
# @admin.register(Medicamento)
# class MedicamentoAdmin(ImportExportMixin, admin.ModelAdmin):
#     search_fields = ['codigo_tuss', 'termo', 'apresentacao', "codigo_anvisa"]
#     list_display = ['codigo_tuss', 'termo', 'apresentacao', "codigo_anvisa"]
#     resource_class = MedicamentoResource
#
# @admin.register(Procedimento)
# class ProcedimentoAdmin(ImportExportMixin, admin.ModelAdmin):
#     search_fields = ['codigo_tuss', 'termo']
#     list_display = ['codigo_tuss', 'termo']
#     resource_class = ProcedimentoResource
#
# @admin.register(Material)
# class MaterialAdmin(ImportExportMixin, admin.ModelAdmin):
#     search_fields = ['codigo_tuss', 'termo', "fabricante", "classe_risco", "nome_tecnico"]
#     list_display = ['codigo_tuss', 'termo', "fabricante", "classe_risco", "nome_tecnico", "codigo_anvisa", "dt_fim_vigencia"]
#     resource_class = MaterialResource
#
# @admin.register(DiariaTaxa)
# class DiariaTaxaAdmin(ImportExportMixin, admin.ModelAdmin):
#     search_fields = ['codigo_tuss', 'termo', "descricao_detalhada",]
#     list_display = ['codigo_tuss', 'termo', "descricao_detalhada",]
#     resource_class = DiariaTaxaResource
#
# @admin.register(DemaisTerminologia)
# class DemaisTerminologiaAdmin(ImportExportMixin, admin.ModelAdmin):
#     search_fields = ['codigo_tuss', 'termo', 'tabela']
#     list_display = ['codigo_tuss', 'termo','tabela']
#     resource_class = DemaisTerminologiaResource