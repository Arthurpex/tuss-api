from pprint import pprint
from typing import List

from elasticsearch import RequestError
from elasticsearch_dsl import Search
from elasticsearch_dsl.query import MultiMatch, Q, MoreLikeThis

from tuss_items.documents import TermoTussDocument


def get_search_results(query, fields: List[str], tabelas: List, count):
    if not count or count == "":
        count = 100

    if not fields:
        fields = [
            "termo",
            "related_model.laboratorio",
            "related_model.modelo",
            "related_model.fabricante",
            "related_model.nome_tecnico",
            "related_model.apresentacao",
            "related_model.codigo_anvisa",
            "codigo_tuss",
        ]

    text_fields = [
        field
        for field in fields
        if field not in ["codigo_tuss", "related_model.codigo_anvisa"]
    ]

    long_fields = [
        field
        for field in fields
        if field in ["codigo_tuss", "related_model.codigo_anvisa"]
    ]

    should_query = []

    if query.isdigit() and long_fields:
        long_query = Q(
            "bool", should=[Q("match", **{field: int(query)}) for field in long_fields]
        )
        should_query.append(long_query)

    if text_fields:
        text_query = Q(
            "multi_match",
            query=query,
            fields=text_fields,
            type="best_fields",
            fuzziness=1,
        )
        should_query.append(text_query)

    if not should_query:
        should_query = [Q("match_none")]

    combined_query = Q("bool", should=should_query)

    s = TermoTussDocument.search().query(combined_query).extra(size=count)

    s = s.highlight(*fields, fragment_size=0)

    if tabelas:
        tabela_queries = [Q("term", **{"tabela": tabela}) for tabela in tabelas]
        s = s.query("bool", filter=tabela_queries)

    response = s.execute()

    queryset = []
    for hit in response:
        hit_dict = hit.to_dict()

        extra_fields = {}
        match_fields = []

        for field in fields:
            field_name = field.replace("related_model.", "")
            if field_name in hit_dict.get("related_model", {}):
                extra_fields[field_name] = hit_dict["related_model"][field_name]

            if "highlight" in hit.meta and field in hit.meta.highlight:
                match_fields.append(field.replace("related_model.", ""))

        item = {
            "score": hit.meta.score,
            "id": hit.id,
            "codigo_tuss": hit.codigo_tuss,
            "tabela": hit.tabela,
            "termo": hit.termo,
            "dt_inicio_vigencia": hit.dt_inicio_vigencia,
            "dt_fim_vigencia": hit.dt_fim_vigencia,
            "dt_implantacao": hit.dt_implantacao,
            "extra_fields": extra_fields,
            "match_fields": match_fields,
        }
        queryset.append(item)

    return queryset




def get_suggestions(query, fields, tabelas):
    """Best implementation so far"""
    default_fields = [
        "termo.suggest",
        "related_model.laboratorio",
        "related_model.modelo",
        "related_model.fabricante",
        "related_model.nome_tecnico",
        "related_model.apresentacao",
    ]

    if (
        fields == ["codigo_tuss"]
        or fields == ["related_model.codigo_anvisa"]
        or fields == ["codigo_tuss", "related_model.codigo_anvisa"]
    ):
        return []

    if "codigo_tuss" in fields:
        fields.remove("codigo_tuss")

    if "related_model.codigo_anvisa" in fields:
        fields.remove("related_model.codigo_anvisa")

    words = query.split()
    s = TermoTussDocument.search()

    if not fields:
        fields = default_fields

    s = s.query(
        "bool",
        should=[
            Q("multi_match", query=word, type="phrase_prefix", fields=fields)
            for word in words
        ],
    )

    # Use the highlight method to mark the fields where the matches occurred
    s = s.highlight(*fields, fragment_size=0)

    s = s.extra(size=10)

    if tabelas:
        tabela_queries = [Q("term", tabela=tabela) for tabela in tabelas]
        s = s.query("bool", should=tabela_queries, minimum_should_match=1)

    response = s.execute()

    results = []
    for hit in response:
        # Initialize matches as an empty list
        matches = []

        # Check if the field has highlights
        if "highlight" in hit.meta:
            for field in hit.meta.highlight:
                for match in hit.meta.highlight[field]:
                    # Remove the highlight tags
                    match = match.replace("<em>", "").replace("</em>", "")
                    matches.append(
                        {
                            "id": hit.id,
                            "match": match,
                            "field": field,
                        }
                    )

        # If there are any matches, add them to the results
        if matches:
            results.extend(matches)

    return results
