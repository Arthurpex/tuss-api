from django.http import JsonResponse
from django_elasticsearch_dsl_drf.filter_backends import FilteringFilterBackend, OrderingFilterBackend, \
    DefaultOrderingFilterBackend, SearchFilterBackend
from django_elasticsearch_dsl_drf.viewsets import BaseDocumentViewSet, DocumentViewSet
from elasticsearch import Elasticsearch
from elasticsearch_dsl import Q, MultiSearch, Search
from elasticsearch_dsl import connections

from rest_framework import viewsets, status, views
from rest_framework.response import Response
from rest_framework.views import APIView

from .documents import MaterialDocument, MedicamentoDocument
from .models import Medicamento, Material, DiariaTaxa, Procedimento, DemaisTerminologia, Tabela87
from .serializers import MedicamentoSerializer, MaterialSerializer, DiariaTaxaSerializer, ProcedimentoSerializer, \
    DemaisTerminologiaSerializer, TabelasSerializer, MaterialDocumentSerializer, MedicamentoDocumentSerializer


class MedicamentoViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Medicamento.objects.all()
    serializer_class = MedicamentoSerializer


class MaterialViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Material.objects.all()
    serializer_class = MaterialSerializer


class DiariaTaxaViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = DiariaTaxa.objects.all()
    serializer_class = DiariaTaxaSerializer


class ProcedimentoViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Procedimento.objects.all()
    serializer_class = ProcedimentoSerializer


class DemaisTerminologiaViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = DemaisTerminologia.objects.all()
    serializer_class = DemaisTerminologiaSerializer


class TabelasViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tabela87.objects.all()
    serializer_class = TabelasSerializer


# class MedicamentoSearchViewSet(BaseDocumentViewSet):
#     document = MedicamentoDocument
#     serializer_class = MedicamentoSearchSerializer
#     filter_backends = [
#         CompoundSearchFilterBackend,
#         OrderingFilterBackend,
#         FilteringFilterBackend,
#     ]
#     search_fields = (
#         # 'tabela',
#         'codigo_tuss',
#         'termo',
#         'apresentacao',
#         'laboratorio',
#         'codigo_anvisa',
#     )
#     filter_fields = {
#         "termo": "termo",
#         "apresentacao": "apresentacao",
#         "laboratorio": "laboratorio",
#         "codigo_anvisa": "codigo_anvisa",
#     }
#     ordering_fields = {
#         "termo": "termo",
#         "codigo_anvisa": "codigo_anvisa",
#     }
#     ordering = ("-termo",)
#
#     def get_queryset(self):
#         queryset = super().get_queryset()
#         search_query = self.request.query_params.get("q", None)
#         if search_query is not None:
#             search = Q(
#                 "multi_match",
#                 query=search_query,
#                 fields=self.search_fields,
#                 fuzziness="AUTO",
#             )
#             queryset = queryset.query(search)
#         # Set the size parameter to 20 to return 20 results
#         queryset = queryset[:5]
#         return queryset

#
# class SearchView(APIView):
#     document_models = {
#         18: DiariaTaxaDocument,
#         19: MaterialDocument,
#         20: MedicamentoDocument,
#         22: ProcedimentoDocument,
#         59: Tabela59Document,
#         60: Tabela60Document,
#         79: Tabela79Document,
#         81: Tabela81Document,
#         63: Tabela63Document,
#         # 64: Tabela64Document,
#         87: Tabela87Document
#     }
#
#     search_fields = [
#         'codigo_tuss',
#         'termo',
#         'apresentacao',
#         'laboratorio',
#         'codigo_anvisa',
#         # add fields for DiariaTaxaDocument and ProcedimentoDocument
#     ]
#
#     def get(self, request):
#         search_query = request.query_params.get("q")
#         tabela = request.query_params.get("tabela")
#
#         if not search_query:
#             return Response({"error": "No search query provided."}, status=status.HTTP_400_BAD_REQUEST)
#
#         if tabela:
#             try:
#                 tabela = int(tabela)
#             except ValueError:
#                 return Response({"error": "Invalid tabela parameter."}, status=status.HTTP_400_BAD_REQUEST)
#             if tabela not in self.document_models:
#                 return Response({"error": "Invalid tabela parameter."}, status=status.HTTP_400_BAD_REQUEST)
#
#
#         if tabela:
#             s = Search(index=self.document_models[tabela])
#         else:
#             s = Search(index="*")
#
#         # Create a multi-match query to search across all fields.
#         query = Q("multi_match", query=search_query, fields=self.search_fields)
#         s = s.query(query)
#
#         print(s.to_dict())
#
#         # Execute the search
#         response = s.execute()
#
#         # Format the results for the response
#         results = []
#         for hit in response:
#             results.append(hit.to_dict())
#
#         return Response({"results": results}, status=status.HTTP_200_OK)
#

class GeneralSearchView(APIView):
    document_models = [
        MedicamentoDocument,
        MaterialDocument,
        # ... add your other document models here
    ]

    def get(self, request):
        query = request.query_params.get("q", None)
        if not query:
            return Response({"error": "No query provided."}, status=status.HTTP_400_BAD_REQUEST)

        connections.create_connection(
            hosts=['https://localhost'],
            http_auth=('elastic', 'ZgiunzKO5TqmS3mKWtW+'),
            scheme="https",
            port=9200,
            timeout=20
        )

        ms = MultiSearch()
        for Doc in self.document_models:
            s = Search(index=Doc._index._name).query("multi_match", query=query, fields=["*"])
            ms = ms.add(s)

        responses = ms.execute()

        results = []
        for response in responses:
            for hit in response:
                result = hit.to_dict()
                result['_type'] = hit.meta.index  # Include the document type in the result
                results.append(result)

        return Response(results)