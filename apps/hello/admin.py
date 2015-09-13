from django.contrib import admin

from .models import Bio


class BioAdmin(admin.ModelAdmin):
    pass


admin.site.register(Bio, BioAdmin)
