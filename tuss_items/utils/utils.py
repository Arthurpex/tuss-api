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
        match = result["match"]

        # If this match hasn't been seen before, keep it and mark it as seen
        if match not in seen_matches:
            filtered_results.append(result)
            seen_matches.add(match)

    return filtered_results
