from typing import List

from django.core.paginator import Paginator
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.pagination import PageNumberPagination, CursorPagination
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
from urllib.parse import urlencode, unquote


def get_search_fields(fields, field_mapping):
    search_fields = []
    invalid_fields = []
    for field in fields:
        field_exists = field_mapping.get(field)
        if field_exists:
            search_fields.append(field_exists)
        else:
            invalid_fields.append(field)
    return search_fields, invalid_fields


def get_filter_tabelas(tabelas, tabelas_allowed):
    filter_tabelas = []
    invalid_tabelas = []
    for tabela in tabelas:
        if int(tabela) in tabelas_allowed:
            filter_tabelas.append(tabela)
        else:
            invalid_tabelas.append(tabela)
    return filter_tabelas, invalid_tabelas


def get_paginated_response(request, queryset, size=10):
    page = request.query_params.get("page", default=1)
    page = int(page)
    page_size = size

    start_index = (page - 1) * page_size
    end_index = start_index + page_size
    page_data = queryset[start_index:end_index]

    base_url = request.build_absolute_uri().split("?")[0]
    query_params = request.GET.copy()
    if end_index < len(queryset):
        query_params["page"] = page + 1
        next_url = base_url + "?" + urlencode(query_params)
    else:
        next_url = None

    if page > 1:
        query_params["page"] = page - 1
        previous_url = base_url + "?" + urlencode(query_params)
    else:
        previous_url = None

    return {
        "count": len(queryset),
        "next": next_url,
        "previous": previous_url,
        "results": page_data,
    }

def filter_duplicates(results):
    seen_matches = set()
    filtered_results = []

    for result in results:
        match = result['match']

        # If this match hasn't been seen before, keep it and mark it as seen
        if match not in seen_matches:
            filtered_results.append(result)
            seen_matches.add(match)

    return filtered_results

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

        tabelas_allowed = [
            18,
            19,
            20,
            22,
            23,
            24,
            25,
            26,
            27,
            28,
            29,
            30,
            31,
            32,
            33,
            34,
            35,
            36,
            37,
            38,
            39,
            40,
            41,
            42,
            43,
            44,
            45,
            46,
            47,
            48,
            49,
            50,
            51,
            52,
            53,
            54,
            55,
            56,
            57,
            58,
            59,
            60,
            61,
            62,
            63,
            64,
            65,
            66,
            67,
            68,
            69,
            70,
            71,
            72,
            73,
            74,
            87,
            90,
            98,
            75,
            76,
            77,
            78,
            79,
            80,
            81,
        ]

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

        tabelas_allowed = [
            18,
            19,
            20,
            22,
            23,
            24,
            25,
            26,
            27,
            28,
            29,
            30,
            31,
            32,
            33,
            34,
            35,
            36,
            37,
            38,
            39,
            40,
            41,
            42,
            43,
            44,
            45,
            46,
            47,
            48,
            49,
            50,
            51,
            52,
            53,
            54,
            55,
            56,
            57,
            58,
            59,
            60,
            61,
            62,
            63,
            64,
            65,
            66,
            67,
            68,
            69,
            70,
            71,
            72,
            73,
            74,
            87,
            90,
            98,
            75,
            76,
            77,
            78,
            79,
            80,
            81,
        ]

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


class TermoTussViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = TermoTuss.objects.all()

    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["tabela", "codigo_tuss"]

    def get_serializer_class(self):
        if self.action == "retrieve":
            return SingleTermoTussSerializer
        return TermoTussSerializer


class TabelasViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = TabelasDominio.objects.all()
    serializer_class = TabelasSerializer


class GruposViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = GrupoEnvio.objects.all()
    serializer_class = GrupoEnvioSerializer
