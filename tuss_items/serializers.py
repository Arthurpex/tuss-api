from django_elasticsearch_dsl_drf.serializers import DocumentSerializer

from .documents import TermoTussDocument

from .models import (
    Medicamento,
    Material,
    DiariaTaxa,
    Procedimento,
    DemaisTerminologia,
    TabelasDominio,
    GrupoEnvio,
    FormaEnvio,
    UnidadeMedida,
    UnidadeFederacao,
    TipoDocumento,
    TermoTuss,
    ModeloRemuneracao,
)

from rest_framework import serializers

from .utils.anvisa import get_anvisa_data


class TabelasSerializer(serializers.ModelSerializer):
    class Meta:
        model = TabelasDominio
        fields = "__all__"


class GrupoEnvioSerializer(serializers.ModelSerializer):
    class Meta:
        model = GrupoEnvio
        fields = "__all__"


class FormaEnvioSerializer(serializers.ModelSerializer):
    class Meta:
        model = FormaEnvio
        fields = "__all__"


class MedicamentoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Medicamento
        fields = ["apresentacao", "laboratorio", "codigo_anvisa"]


class MaterialSerializer(serializers.ModelSerializer):
    class Meta:
        model = Material
        fields = [
            "modelo",
            "fabricante",
            "codigo_anvisa",
            "classe_risco",
            "nome_tecnico",
        ]


class ProcedimentoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Procedimento
        fields = ["descricao_detalhada"]


class DiariaTaxaSerializer(serializers.ModelSerializer):
    class Meta:
        model = DiariaTaxa
        fields = ["descricao_detalhada"]


class DemaisTerminologiaSerializer(serializers.ModelSerializer):
    class Meta:
        model = DemaisTerminologia
        fields = []


class UnidadeFederacaoSerializer(serializers.ModelSerializer):
    class Meta:
        model = UnidadeFederacao
        fields = ["sigla"]


class UnidadeMedidaSerializer(serializers.ModelSerializer):
    class Meta:
        model = UnidadeMedida
        fields = ["descricao_detalhada"]


class ModeloRemuneracaoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ModeloRemuneracao
        fields = ["descricao_detalhada"]


class TipoDocumentoSerializer(serializers.ModelSerializer):
    class Meta:
        model = TipoDocumento
        fields = ["requer_assinatura"]


class TermoTussSerializer(serializers.ModelSerializer):
    class Meta:
        model = TermoTuss
        fields = [
            "id",
            "codigo_tuss",
            "tabela",
            "termo",
            "dt_inicio_vigencia",
            "dt_fim_vigencia",
            "dt_implantacao",
        ]


class SingleTermoTussSerializer(serializers.ModelSerializer):
    extra_fields = serializers.SerializerMethodField()
    forma_de_envio = serializers.SerializerMethodField()
    grupo = serializers.SerializerMethodField()


    class Meta:
        model = TermoTuss
        fields = [
            "id",
            "codigo_tuss",
            "tabela",
            "termo",
            "dt_inicio_vigencia",
            "dt_fim_vigencia",
            "dt_implantacao",
            "forma_de_envio",
            "grupo",
            "extra_fields",
        ]

    def get_extra_fields(self, obj):
        if obj.tabela == 18:
            return DiariaTaxaSerializer(obj.diariataxa).data
        elif obj.tabela == 19:
            return MaterialSerializer(obj.material).data
        elif obj.tabela == 20:
            return MedicamentoSerializer(obj.medicamento).data
        elif obj.tabela == 22:
            return ProcedimentoSerializer(obj.procedimento).data
        elif obj.tabela == 59:
            return UnidadeFederacaoSerializer(obj.tabela59).data
        elif obj.tabela == 60:
            return UnidadeMedidaSerializer(obj.tabela60).data
        elif obj.tabela == 79:
            return ModeloRemuneracaoSerializer(obj.tabela79).data
        elif obj.tabela == 81:
            return TipoDocumentoSerializer(obj.tabela81).data
        else:
            return None

    def get_forma_de_envio(self, obj):
        # Fetch the Tabela64 model instance filtered by codigo_tuss and terminologia
        tabela64 = FormaEnvio.objects.filter(
            codigo_tuss=obj.codigo_tuss, terminologia=obj.tabela
        ).first()

        # Return the forma_de_envio attribute of the Tabela64 instance, if it exists
        return tabela64.forma_de_envio if tabela64 else None

    def get_grupo(self, obj):
        # Fetch the Tabela64 model instance filtered by codigo_tuss and terminologia
        tabela64 = FormaEnvio.objects.filter(
            codigo_tuss=obj.codigo_tuss, terminologia=obj.tabela
        ).first()

        # Return the forma_de_envio attribute of the Tabela64 instance, if it exists
        return tabela64.codigo_do_grupo if tabela64 else None


