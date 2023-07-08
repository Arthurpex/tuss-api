from django.db import models


class TermoTuss(models.Model):
    codigo_tuss = models.CharField(null=False, max_length=256)
    tabela = models.IntegerField(null=False)

    termo = models.TextField(null=False)
    dt_inicio_vigencia = models.DateTimeField(null=False)
    dt_fim_vigencia = models.DateTimeField(null=True)
    dt_implantacao = models.DateTimeField(null=True)

    class Meta:
        unique_together = ("codigo_tuss", "tabela")


class Medicamento(models.Model):
    termo_tuss = models.OneToOneField(TermoTuss, on_delete=models.CASCADE)

    apresentacao = models.CharField(null=False, max_length=256)
    laboratorio = models.CharField(null=False, max_length=256)
    codigo_anvisa = models.CharField(null=False, max_length=256)


class Material(models.Model):
    termo_tuss = models.OneToOneField(TermoTuss, on_delete=models.CASCADE)

    modelo = models.TextField(null=False)
    fabricante = models.TextField(null=False)
    codigo_anvisa = models.CharField(null=False, max_length=256)
    classe_risco = models.CharField(null=False, max_length=256)
    nome_tecnico = models.TextField(null=False)


class Procedimento(models.Model):
    termo_tuss = models.OneToOneField(TermoTuss, on_delete=models.CASCADE)

    descricao_detalhada = models.TextField(null=True, blank=True)


class DiariaTaxa(models.Model):
    termo_tuss = models.OneToOneField(TermoTuss, on_delete=models.CASCADE)

    descricao_detalhada = models.TextField(null=True, blank=True)


class DemaisTerminologia(models.Model):
    termo_tuss = models.OneToOneField(TermoTuss, on_delete=models.CASCADE)


class UnidadeFederacao(models.Model):
    termo_tuss = models.OneToOneField(TermoTuss, on_delete=models.CASCADE)

    sigla = models.CharField(null=False, max_length=256)


class UnidadeMedida(models.Model):
    termo_tuss = models.OneToOneField(TermoTuss, on_delete=models.CASCADE)

    descricao_detalhada = models.TextField(null=True)


class ModeloRemuneracao(models.Model):
    termo_tuss = models.OneToOneField(TermoTuss, on_delete=models.CASCADE)

    descricao_detalhada = models.TextField(null=True)


class TipoDocumento(models.Model):
    termo_tuss = models.OneToOneField(TermoTuss, on_delete=models.CASCADE)

    requer_assinatura = models.CharField(null=True, max_length=256)


class GrupoEnvio(models.Model):
    tabela = models.IntegerField(null=False)

    codigo = models.CharField(null=False, max_length=256)
    grupo = models.CharField(null=False, max_length=256)
    dt_inicio_vigencia = models.DateTimeField(null=False)
    dt_fim_vigencia = models.DateTimeField(null=True)
    dt_implantacao = models.DateTimeField(null=True)


class FormaEnvio(models.Model):
    codigo_tuss = models.CharField(null=False, max_length=256)
    terminologia = models.CharField(null=False, max_length=256)
    forma_de_envio = models.CharField(null=False, max_length=256)
    codigo_do_grupo = models.IntegerField(null=True)


class TabelasDominio(models.Model):
    codigo_tabela = models.IntegerField(null=False)

    descricao = models.CharField(null=False, max_length=256)

    dt_inicio_vigencia = models.DateTimeField(null=False)
    dt_fim_vigencia = models.DateTimeField(null=True)
    dt_implantacao = models.DateTimeField(null=True)
