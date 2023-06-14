from pprint import pprint
from typing import List

from elasticsearch import RequestError
from elasticsearch_dsl import Search
from elasticsearch_dsl.query import MultiMatch, Q, MoreLikeThis

from tuss_items.documents import TermoTussDocument


#
# def get_search_results(query, tabela=None):
#     fields = [
#         'termo',
#         'related_model.laboratorio',
#         'related_model.modelo',
#         'related_model.fabricante',
#         'related_model.codigo_anvisa',
#         'related_model.nome_tecnico',
#         'related_model.apresentacao',
#     ]
#
#     q = Q(MultiMatch(query=query, fields=fields, type='best_fields', fuzziness='AUTO'))
#
#     s = TermoTussDocument.search().query(q)
#
#     if tabela is not None:
#         s = s.filter('term', tabela=tabela)
#
#     results = s.execute()
#
#     queryset = []
#     for hit in results:
#         hit_dict = hit.to_dict()
#
#
#         item = {
#             'codigo_tuss': hit.codigo_tuss,
#             'tabela': hit.tabela,
#             'termo': hit.termo,
#             'dt_inicio_vigencia': hit.dt_inicio_vigencia,
#             'dt_fim_vigencia': hit.dt_fim_vigencia,
#             'dt_implantacao': hit.dt_implantacao,
#             'extra_fields': hit_dict.get('related_model', {}),  # Retrieve related_model from the dict
#         }
#         queryset.append(item)
#
#     return queryset
#


def get_search_results_working_old(query, fields: List[str], tabelas: List, count):
    if not fields:
        fields = [
            "termo",
            # "codigo_tuss",
            "related_model.laboratorio",
            "related_model.modelo",
            "related_model.fabricante",
            # 'related_model.codigo_anvisa',
            "related_model.nome_tecnico",
            "related_model.apresentacao",
        ]

    if not count:
        count = 10

    q = Q(MultiMatch(query=query, fields=fields, type="best_fields", fuzziness="AUTO"))

    s = TermoTussDocument.search().query(q).extra(size=count)  # limit to 15 results

    if tabelas:
        tabela_queries = [Q("term", tabela=tabela) for tabela in tabelas]
        s = s.query("bool", should=tabela_queries, minimum_should_match=1)

    results = s.execute()

    queryset = []
    for hit in results:
        hit_dict = hit.to_dict()

        # Initialize extra_fields with an empty dictionary
        extra_fields = {}

        # Only add the fields to extra_fields if they are present in the hit
        for field in fields:
            # Remove 'related_model.' from the field name
            field_name = field.replace("related_model.", "")
            if field_name in hit_dict.get("related_model", {}):
                extra_fields[field_name] = hit_dict["related_model"][field_name]

        item = {
            "score": hit.meta.score,
            "codigo_tuss": hit.codigo_tuss,
            "tabela": hit.tabela,
            "termo": hit.termo,
            "dt_inicio_vigencia": hit.dt_inicio_vigencia,
            "dt_fim_vigencia": hit.dt_fim_vigencia,
            "dt_implantacao": hit.dt_implantacao,
            "extra_fields": extra_fields,  # Use the adjusted extra_fields
        }
        queryset.append(item)

    return queryset


# improved current
def get_search_results_working(query, fields: List[str], tabelas: List, count):
    if not count or count == "":
        count = 10

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

    text_query = Q(
        "multi_match",
        query=query,
        fields=text_fields,
        type="best_fields",
        fuzziness="AUTO",
    )

    should_query = [text_query]

    long_query = Q(
        "bool", should=[Q("match", **{field: int(query)}) for field in long_fields]
    )
    should_query.append(long_query)

    combined_query = Q("bool", should=should_query)

    s = TermoTussDocument.search().query(combined_query).extra(size=count)

    if tabelas:
        tabela_queries = [Q("term", tabela=tabela) for tabela in tabelas]
        s = s.query("bool", should=tabela_queries, minimum_should_match=1)

    response = s.execute()

    queryset = []
    for hit in response:
        hit_dict = hit.to_dict()

        # Initialize extra_fields with an empty dictionary
        extra_fields = {}

        # Only add the fields to extra_fields if they are present in the hit
        for field in fields:
            # Remove 'related_model.' from the field name
            field_name = field.replace("related_model.", "")
            if field_name in hit_dict.get("related_model", {}):
                extra_fields[field_name] = hit_dict["related_model"][field_name]

        item = {
            "score": hit.meta.score,
            "id": hit.id,
            "codigo_tuss": hit.codigo_tuss,
            "tabela": hit.tabela,
            "termo": hit.termo,
            "dt_inicio_vigencia": hit.dt_inicio_vigencia,
            "dt_fim_vigencia": hit.dt_fim_vigencia,
            "dt_implantacao": hit.dt_implantacao,
            "extra_fields": extra_fields,  # Use the adjusted extra_fields
        }
        queryset.append(item)

    return queryset


# Even more improved
def get_search_results_workds(query, fields: List[str], tabelas: List, count):
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

    text_query = Q(
        "multi_match", query=query, fields=text_fields, type="best_fields", fuzziness=1
    )

    should_query = [text_query]

    # Check if the query is numeric before attempting to create and append long_query
    if query.isdigit():
        long_query = Q(
            "bool", should=[Q("match", **{field: int(query)}) for field in long_fields]
        )
        should_query.append(long_query)

    combined_query = Q("bool", should=should_query)

    s = TermoTussDocument.search().query(combined_query).extra(size=count)

    # Use the highlight method to mark the fields where the matches occurred
    s = s.highlight(*fields, fragment_size=0)

    if tabelas:
        tabela_queries = [Q("term", **{"tabela": tabela}) for tabela in tabelas]
        s = s.query("bool", filter=tabela_queries)

    response = s.execute()

    queryset = []
    for hit in response:
        hit_dict = hit.to_dict()

        # Initialize extra_fields with an empty dictionary
        extra_fields = {}

        # Initialize match_fields as an empty list
        match_fields = []

        # Only add the fields to extra_fields if they are present in the hit
        for field in fields:
            # Remove 'related_model.' from the field name
            field_name = field.replace("related_model.", "")
            if field_name in hit_dict.get("related_model", {}):
                extra_fields[field_name] = hit_dict["related_model"][field_name]

            # If the field has highlights, add it to match_fields
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
            "extra_fields": extra_fields,  # Use the adjusted extra_fields
            "match_fields": match_fields,  # Add match_fields to the item
        }
        queryset.append(item)

    return queryset


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


def get_suggestions_best(query, fields):
    default_fields = [
        "termo.suggest",
        "related_model.laboratorio",
        "related_model.modelo",
        "related_model.fabricante",
        "related_model.nome_tecnico",
        "related_model.apresentacao",
    ]

    words = query.split()
    s = TermoTussDocument.search()

    if not fields:
        fields = default_fields

    for word in words:
        s = s.query(
            "bool",
            should=[
                {
                    "multi_match": {
                        "query": word,
                        # 'type': 'phrase_prefix',
                        "type": "bool_prefix",
                        "fields": fields,
                    }
                }
                for word in words
            ],
        )

    # Use the highlight method to mark the fields where the matches occurred
    s = s.highlight(*fields, fragment_size=0)

    response = s.execute()

    results = []
    for hit in response:
        hit_dict = hit.to_dict()

        # Initialize match_fields as an empty list
        match_fields = []

        # Only add the fields to extra_fields if they are present in the hit
        for field in fields:
            # If the field has highlights, add it to match_fields
            if "highlight" in hit.meta and field in hit.meta.highlight:
                match_fields.append(field)

        item = {
            "termo": hit.termo,
            "match_fields": match_fields,  # Add match_fields to the item
        }

        results.append(item)

    return results


def get_suggestions__idk(query, fields):
    default_fields = [
        "termo.suggest",
        # Assuming extra_fields has 'search_as_you_type' fields
        "related_model.laboratorio",
        "extra_fields.laboratorio",
        "extra_fields.modelo",
        "extra_fields.fabricante",
        "extra_fields.nome_tecnico",
        "extra_fields.apresentacao",
    ]

    words = query.split()
    s = TermoTussDocument.search()

    if not fields:
        fields = default_fields

    for word in words:
        s = s.query(
            "bool",
            should=[
                {
                    "multi_match": {
                        "query": word,
                        "type": "bool_prefix",
                        "fields": fields,
                    }
                }
                for word in words
            ],
        )
    s = s.highlight(*fields, fragment_size=0)

    response = s.execute()

    #
    results = []
    for hit in response:
        result = {}
        if "highlight" in hit.meta:
            print(hit.meta.highlight)
            for field, highlight in hit.meta.highlight.items():
                pass
        results.append(result)

    return results


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

    # Get suggestions only for the first 30 results
    s = s.extra(size=30)

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
