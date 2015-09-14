from django.shortcuts import render
from django.core.management import call_command

from .models import Bio


def main(request):
    call_command('loaddata', 'initial_data')
    return render(request, 'main.html', {'bio': Bio.objects.first()})
