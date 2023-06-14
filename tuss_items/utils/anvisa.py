from json import JSONDecodeError
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

    try:
        response = requests.get(url, headers=headers, verify=False)
        response.raise_for_status()
    except requests.exceptions.HTTPError as http_err:
        return {"error": f"HTTP error occurred: {http_err}"}
    except requests.exceptions.RequestException as err:
        return {"error": f"Error occurred: {err}"}

    try:
        return response.json().get('content', [{}])[0].get('processo')
    except JSONDecodeError:
        return {"error": "Error decoding the response"}


def get_anvisa_detail_data(processo):
    url = urljoin(settings.ANVISA_URL, f"saude/{processo}")
    headers = {"Authorization": "Guest"}

    try:
        detail_response = requests.get(url, headers=headers, verify=False)
        detail_response.raise_for_status()
    except requests.exceptions.HTTPError as http_err:
        return {"error": f"HTTP error occurred: {http_err}"}
    except requests.exceptions.RequestException as err:
        return {"error": f"Error occurred: {err}"}

    try:
        return detail_response.json()
    except JSONDecodeError:
        return {"error": "Error decoding the response"}


def get_anvisa_data(numeroRegistro):
    processo = get_anvisa_base_data(numeroRegistro)
    if "error" in processo:
        return processo

    return get_anvisa_detail_data(processo)
