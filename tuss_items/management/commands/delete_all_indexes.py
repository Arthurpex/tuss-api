from django.conf import settings
from django.core.management import BaseCommand
from elasticsearch_dsl.connections import connections

class Command(BaseCommand):
    def handle(self, *args, **options):
        connections.create_connection(**settings.ELASTICSEARCH_DSL["default"])

        es = connections.get_connection()
        es.indices.delete(index="termo_tuss", ignore=[400, 404])
