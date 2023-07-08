




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

