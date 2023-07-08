from django.conf import settings
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, pagination
from rest_framework.decorators import api_view
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import GrupoEnvio, TabelasDominio, TermoTuss
from .search import get_search_results, get_suggestions
from .serializers import (
    TabelasSerializer,
    TermoTussSerializer,
    SingleTermoTussSerializer,
    GrupoEnvioSerializer,
)
from urllib.parse import unquote

from .utils.anvisa import get_anvisa_data
from .utils.utils import (
    get_search_fields,
    get_filter_tabelas,
    get_paginated_response,
    filter_duplicates,
)


class SearchViewSet(APIView):
    serializer_class = TermoTussSerializer
    filterset_fields = ["codigo_tuss"]

    def get(self, request, *args, **kwargs):
        query = request.GET.get("query", "")

        if not query:
            return Response({"detail": "query parameter is required"}, status=400)

        tabela_param = unquote(request.GET.get("tabelas", ""))
        fields_param = unquote(request.GET.get("fields", ""))
        count = unquote(request.GET.get("count", ""))

        fields = fields_param.split(",") if fields_param else []
        tabelas = tabela_param.split(",") if tabela_param else []

        field_mapping = {
            "termo": "termo",
            "laboratorio": "related_model.laboratorio",
            "modelo": "related_model.modelo",
            "fabricante": "related_model.fabricante",
            "nome_tecnico": "related_model.nome_tecnico",
            "apresentacao": "related_model.apresentacao",
            "codigo_tuss": "codigo_tuss",
            "codigo_anvisa": "related_model.codigo_anvisa",
        }

        tabelas_allowed = settings.TABELAS_ALLOWED

        search_fields, invalid_fields = get_search_fields(fields, field_mapping)
        filter_tabelas, invalid_tabelas = get_filter_tabelas(tabelas, tabelas_allowed)

        if invalid_fields or invalid_tabelas:
            error_message = []
            if invalid_fields:
                error_message.append(f"Invalid fields: {invalid_fields}")
            if invalid_tabelas:
                error_message.append(f"Invalid tabela: {invalid_tabelas}")
            return Response({"error": ", ".join(error_message)})

        fields = [field_mapping.get(field, field) for field in fields]
        fields = [field.replace("\n", "") for field in fields]

        queryset = get_search_results(query, fields, filter_tabelas, count)

        response = get_paginated_response(request, queryset)
        return Response(response)


class AutoCompleteViewSet(APIView):
    def get(self, request, *args, **kwargs):
        query = request.GET.get("query", "")

        if not query:
            return Response({"detail": "query parameter is required"}, status=400)

        tabela_param = unquote(request.GET.get("tabelas", ""))
        fields_param = unquote(request.GET.get("fields", ""))

        tabelas_allowed = settings.TABELAS_ALLOWED

        fields = fields_param.split(",") if fields_param else []
        tabelas = tabela_param.split(",") if tabela_param else []

        field_mapping = {
            "termo": "termo.suggest",
            "laboratorio": "related_model.laboratorio",
            "modelo": "related_model.modelo",
            "fabricante": "related_model.fabricante",
            "nome_tecnico": "related_model.nome_tecnico",
            "apresentacao": "related_model.apresentacao",
            "codigo_tuss": "codigo_tuss",
            "codigo_anvisa": "related_model.codigo_anvisa",
        }
        search_fields, invalid_fields = get_search_fields(fields, field_mapping)
        filter_tabelas, invalid_tabelas = get_filter_tabelas(tabelas, tabelas_allowed)

        if invalid_fields or invalid_tabelas:
            error_message = []
            if invalid_fields:
                error_message.append(f"Invalid fields: {invalid_fields}")
            if invalid_tabelas:
                error_message.append(f"Invalid tabela: {invalid_tabelas}")
            return Response({"error": ", ".join(error_message)})

        fields = [field_mapping.get(field, field) for field in fields]
        fields = [field.replace("\n", "") for field in fields]

        queryset = get_suggestions(query, fields, tabelas)
        queryset = filter_duplicates(queryset)

        response = get_paginated_response(request, queryset, size=30)

        return Response(response)


# class BaseViewSet(APIView):
#     field_mapping = {}
#
#     def get_params(self, request):
#         query = request.GET.get("query", "")
#         if not query:
#             return Response({"detail": "query parameter is required"}, status=400)
#
#         tabela_param = unquote(request.GET.get("tabelas", ""))
#         fields_param = unquote(request.GET.get("fields", ""))
#
#         fields = fields_param.split(",") if fields_param else []
#         tabelas = tabela_param.split(",") if tabela_param else []
#
#         tabelas_allowed = settings.TABELAS_ALLOWED
#
#         search_fields, invalid_fields = get_search_fields(fields, self.field_mapping)
#         filter_tabelas, invalid_tabelas = get_filter_tabelas(tabelas, tabelas_allowed)
#
#         if invalid_fields or invalid_tabelas:
#             error_message = []
#             if invalid_fields:
#                 error_message.append(f"Invalid fields: {invalid_fields}")
#             if invalid_tabelas:
#                 error_message.append(f"Invalid tabela: {invalid_tabelas}")
#             return Response({"error": ", ".join(error_message)})
#
#         fields = [self.field_mapping.get(field, field) for field in fields]
#         fields = [field.replace("\n", "") for field in fields]
#
#         return query, fields, filter_tabelas
#
#     def process_query(self, request, process_func, *args, **kwargs):
#         query, fields, tabelas = self.get_params(request)
#
#         queryset = process_func(query, fields, tabelas, *args, **kwargs)
#         response = get_paginated_response(request, queryset)
#
#         return Response(response)
#
#
# class SearchViewSet(BaseViewSet):
#     serializer_class = TermoTussSerializer
#     filterset_fields = ["codigo_tuss"]
#
#     field_mapping = {
#         "termo": "termo",
#         "laboratorio": "related_model.laboratorio",
#         "modelo": "related_model.modelo",
#         "fabricante": "related_model.fabricante",
#         "nome_tecnico": "related_model.nome_tecnico",
#         "apresentacao": "related_model.apresentacao",
#         "codigo_tuss": "codigo_tuss",
#         "codigo_anvisa": "related_model.codigo_anvisa",
#     }
#
#     def get(self, request, *args, **kwargs):
#         return self.process_query(request, get_search_results)
#
#
# class AutoCompleteViewSet(BaseViewSet):
#     field_mapping = {
#         "termo": "termo.suggest",
#         "laboratorio": "related_model.laboratorio",
#         "modelo": "related_model.modelo",
#         "fabricante": "related_model.fabricante",
#         "nome_tecnico": "related_model.nome_tecnico",
#         "apresentacao": "related_model.apresentacao",
#         "codigo_tuss": "codigo_tuss",
#         "codigo_anvisa": "related_model.codigo_anvisa",
#     }
#
#     def get(self, request, *args, **kwargs):
#         response = self.process_query(request, get_suggestions)
#         if 'results' in response.data:
#             response.data['results'] = filter_duplicates(response.data['results'])
#         return response



class TermoTussViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = TermoTuss.objects.all()

    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["tabela", "codigo_tuss"]

    def get_serializer_class(self):
        if self.action == "retrieve":
            return SingleTermoTussSerializer
        return TermoTussSerializer


class TabelasPagination(pagination.PageNumberPagination):
    page_size = 100


class TabelasViewSet(viewsets.ReadOnlyModelViewSet):
    pagination_class = TabelasPagination
    queryset = TabelasDominio.objects.all()
    serializer_class = TabelasSerializer


class GruposViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = GrupoEnvio.objects.all()
    serializer_class = GrupoEnvioSerializer


@api_view(['GET'])
def get_anvisa_info(request, *args, **kwargs):
    termo = get_object_or_404(TermoTuss, tabela__in=[19, 20], id=kwargs.get('id'))  # 19 - MATERIAL, 20 - MEDICAMENTO

    if termo.tabela not in (19, 20):
        return Response({"error": "Termo não encontrado", "status": 404})

    tipo = 'medicamento' if termo.tabela == 20 else 'material'
    codigo_anvisa = getattr(termo, tipo).codigo_anvisa

    data = get_anvisa_data(codigo_anvisa)

    result = data.get('result', [])

    return Response(result, status=data.get('status'))