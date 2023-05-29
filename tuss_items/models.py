from django.db import models


class BaseTuss(models.Model):
    codigo_tuss = models.CharField(null=False, max_length=256)
    tabela = models.IntegerField(null=False)

    termo = models.TextField(null=False)
    dt_inicio_vigencia = models.DateTimeField(null=False)
    dt_fim_vigencia = models.DateTimeField(null=True)
    dt_implantacao = models.DateTimeField(null=True)

    def __str__(self):
        return f"TUSS: {self.codigo_tuss}, {self.termo}"

    class Meta:
        abstract = True
        unique_together = ('codigo_tuss', 'tabela')


class Medicamento(BaseTuss):
    apresentacao = models.CharField(null=False, max_length=256)
    laboratorio = models.CharField(null=False, max_length=256)
    codigo_anvisa = models.CharField(null=False, max_length=256)


class Material(BaseTuss):
    modelo = models.CharField(null=False, max_length=256)
    fabricante = models.CharField(null=False, max_length=256)
    codigo_anvisa = models.CharField(null=False, max_length=256)
    classe_risco = models.CharField(null=False, max_length=256)
    nome_tecnico = models.CharField(null=False, max_length=256)


class Procedimento(BaseTuss):
    descricao_detalhada = models.TextField(null=True, blank=True)


class DiariaTaxa(BaseTuss):
    descricao_detalhada = models.TextField(null=True, blank=True)


class DemaisTerminologia(BaseTuss):
    pass


class Tabela59(BaseTuss):
    sigla = models.CharField(null=False, max_length=256)


class Tabela60(BaseTuss):
    descricao_detalhada = models.TextField(null=True)


class Tabela79(BaseTuss):
    descricao_detalhada = models.TextField(null=True)


class Tabela81(BaseTuss):
    requer_assinatura = models.CharField(null=True, max_length=256)


class Tabela63(models.Model):
    tabela = models.IntegerField(null=False)

    codigo = models.CharField(null=False, max_length=256)
    grupo = models.CharField(null=False, max_length=256)
    dt_inicio_vigencia = models.DateTimeField(null=False)
    dt_fim_vigencia = models.DateTimeField(null=True)
    dt_implantacao = models.DateTimeField(null=True)


class Tabela64(models.Model):
    tabela = models.IntegerField(null=False)

    codigo_tuss = models.CharField(null=False, max_length=256)
    terminologia = models.CharField(null=False, max_length=256)
    forma_de_envio = models.CharField(null=False, max_length=256)
    codigo_do_grupo = models.IntegerField(null=True)
    descricao_do_grupo = models.CharField(null=False, max_length=256)
    dt_inicio_vigencia = models.DateTimeField(null=True)
    dt_fim_vigencia = models.DateTimeField(null=True)
    dt_implantacao = models.DateTimeField(null=True)


class Tabela87(models.Model):
    codigo_tabela = models.IntegerField(null=False)

    descricao = models.CharField(null=False, max_length=256)

    dt_inicio_vigencia = models.DateTimeField(null=False)
    dt_fim_vigencia = models.DateTimeField(null=True)
    dt_implantacao = models.DateTimeField(null=True)
