from django.dispatch import receiver
from django.db.models.signals import post_save, post_delete
from django.db.utils import DatabaseError

from .models import History


@receiver(post_save)    # noqa
def create_or_update_object(sender, instance, created, **kwargs):
    if sender != History:
        try:
            history = History(model_name=instance._meta.model_name,
                              model_instance=instance)
            history.action = History.EDITED
            if created:
                history.action = History.CREATED
            history.save()
        except DatabaseError:
            pass


@receiver(post_delete)  # noqa
def delete_object(sender, instance, **kwargs):
    if sender != History:
        try:
            History.objects.create(model_name=instance._meta.model_name,
                                   model_instance=instance,
                                   action=History.DELETED)
        except DatabaseError:
            pass
