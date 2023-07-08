from urllib.parse import urljoin, urlencode

import requests
from django.conf import settings


def get_anvisa_base_data(numeroRegistro):
    query_params = urlencode({
        "count": 1,
        "filter[numeroRegistro]": numeroRegistro,
        "page": 1
    })
    url = urljoin(settings.ANVISA_URL, f"genericos?{query_params}")
    headers = {"Authorization": "Guest"}

    response = requests.get(url, headers=headers, verify=False)
    response.raise_for_status()

    data = response.json().get('content', [])
    return data[0].get('processo') if len(data) > 0 else None


def get_anvisa_detail_data(processo):
    url = urljoin(settings.ANVISA_URL, f"saude/{processo}")
    headers = {"Authorization": "Guest"}

    detail_response = requests.get(url, headers=headers, verify=False)
    detail_response.raise_for_status()

    return detail_response.json()


def get_anvisa_data(numeroRegistro):
    try:
        processo = get_anvisa_base_data(numeroRegistro)
        print(processo)
        if not processo:
            return {"error": "No data found", "status": 404}  # No Content
        detail_data = get_anvisa_detail_data(processo)
        return {"result": detail_data, "status": 200}  # OK
    except requests.exceptions.HTTPError as http_err:
        return {"error": f"HTTP error occurred: {http_err}", "status": http_err.response.status_code}
    except requests.exceptions.RequestException as err:
        return {"error": f"Error occurred: {err}", "status": 500}  # Internal Server Error
