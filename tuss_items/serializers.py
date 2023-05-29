from django_elasticsearch_dsl_drf.serializers import DocumentSerializer

from .documents import MedicamentoDocument, MaterialDocument
from .models import Medicamento, Material, DiariaTaxa, Procedimento, DemaisTerminologia, Tabela87

from rest_framework import serializers


class MedicamentoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Medicamento
        fields = '__all__'


class MaterialSerializer(serializers.ModelSerializer):
    class Meta:
        model = Material
        fields = '__all__'


class DiariaTaxaSerializer(serializers.ModelSerializer):
    class Meta:
        model = DiariaTaxa
        fields = '__all__'


class ProcedimentoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Procedimento
        fields = '__all__'


class DemaisTerminologiaSerializer(serializers.ModelSerializer):
    class Meta:
        model = DemaisTerminologia
        fields = '__all__'


class TabelasSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tabela87
        fields = '__all__'


class MedicamentoDocumentSerializer(DocumentSerializer):
    class Meta:
        document = MedicamentoDocument
        fields = (
            'codigo_tuss',
            'tabela',
            'termo',

            'apresentacao',
            'laboratorio',
            'codigo_anvisa',
        )


class MaterialDocumentSerializer(DocumentSerializer):
    class Meta:
        document = MaterialDocument
        fields = (
            'codigo_tuss',
            'tabela',
            'termo',
            'modelo',

            'fabricante',
            'codigo_anvisa',
            'classe_risco',
            'nome_tecnico',

        )
