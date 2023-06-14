from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient


class SearchViewSetTests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_search_view_set_filtering(self):
        url = reverse("search")  # Update with your actual endpoint name

        # Test valid filtering
        response = self.client.get(
            url,
            {"fields": "termo,codigo_tuss", "query": "test_query", "tabelas": "18,19"},
        )
        self.assertEqual(response.status_code, 200)
        # Here you can check response.data with expected results

        # Test invalid field
        response = self.client.get(
            url, {"fields": "invalid_field", "query": "test_query", "tabelas": "18,19"}
        )
        self.assertEqual(
            response.status_code, 400
        )  # 400 Bad Request for invalid fields

        # Test invalid tabela
        response = self.client.get(
            url, {"fields": "termo", "query": "test_query", "tabelas": "1000"}
        )
        self.assertEqual(
            response.status_code, 400
        )  # 400 Bad Request for invalid tabelas


class AutoCompleteViewSetTests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_auto_complete_view_set(self):
        url = reverse("autocomplete")  # Update with your actual endpoint name

        # Test valid field
        response = self.client.get(url, {"fields": "termo", "query": "test_query"})
        self.assertEqual(response.status_code, 200)
        # Here you can check response.data with expected results

        # Test invalid field
        response = self.client.get(
            url, {"fields": "invalid_field", "query": "test_query"}
        )
        self.assertEqual(
            response.status_code, 400
        )  # 400 Bad Request for invalid fields
