from elasticsearch_dsl import (
    Document,
    Text,
    analyzer,
    Object,
    Date,
    Integer,
    Keyword,
    Long,
    Completion,
    SearchAsYouType,
)

portuguese_analyzer = analyzer("portuguese")


class ExtraFieldsDocument(Document):
    modelo = Text(analyzer=portuguese_analyzer, fields={"suggest": SearchAsYouType()})
    fabricante = Text(
        analyzer=portuguese_analyzer, fields={"suggest": SearchAsYouType()}
    )
    codigo_anvisa = Long()
    nome_tecnico = Text(
        analyzer=portuguese_analyzer, fields={"suggest": SearchAsYouType()}
    )
    apresentacao = Text(
        analyzer=portuguese_analyzer, fields={"suggest": SearchAsYouType()}
    )
    laboratorio = Text(
        analyzer=portuguese_analyzer, fields={"suggest": SearchAsYouType()}
    )
    descricao_detalhada = Text(analyzer=portuguese_analyzer)
    sigla = Text(analyzer=portuguese_analyzer)


class TermoTussDocument(Document):
    id = Integer()
    codigo_tuss = Long()
    tabela = Integer()
    termo = Text(analyzer=portuguese_analyzer, fields={"suggest": SearchAsYouType()})
    dt_inicio_vigencia = Date()
    dt_fim_vigencia = Date()
    dt_implantacao = Date()
    extra_fields = Object(ExtraFieldsDocument)

    class Index:
        name = "termo_tuss"


# class ExtraFieldsDocument(Document):
#     modelo = Text()
#     fabricante = Text()
#     codigo_anvisa = Text()
#     # classe_risco = Text()
#     nome_tecnico = Text()
#     apresentacao = Text()
#     laboratorio = Text()
#     descricao_detalhada = Text()
#     sigla = Text()
#
#     # requer_assinatura = Text()
#
#     class Index:
#         name = 'extra_fields'
#         settings = {'number_of_shards': 1}
# #
#
#
# class TermoTussDocument(Document):
#     codigo_tuss = Keyword()
#     # codigo_tuss = Text()
#     tabela = Integer()
#     termo = Text()
#     dt_inicio_vigencia = Date()
#     dt_fim_vigencia = Date()
#     dt_implantacao = Date()
#     extra_fields = Object(ExtraFieldsDocument)
#
#     class Index:
#         name = 'termo_tuss'
#         settings = {'number_of_shards': 1}
