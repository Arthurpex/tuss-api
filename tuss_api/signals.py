from django.db.models.signals import post_save
from django.dispatch import receiver

from medicamento.models import Medicamento


@receiver(post_save, sender=Medicamento)
def sync_medicamento_anvisa(
    sender: str, instance: Medicamento, created: bool, **kwargs
):
    pass