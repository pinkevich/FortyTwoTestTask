from django.shortcuts import render

from .models import Bio


def main(request):
    return render(request, 'main.html', {'bio': Bio.objects.first()})
