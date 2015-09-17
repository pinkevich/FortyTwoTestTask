from django.core.management.base import BaseCommand
from django.db.models import get_models


class Command(BaseCommand):
    help = 'Prints all project models and the count of objects in every model'

    def handle(self, *args, **options):
        for model in get_models():
            data = '{0} - {1} records'.format(model.__name__,
                                              model.objects.count())
            self.stdout.write(data)
