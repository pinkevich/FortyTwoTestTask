from django.contrib import admin

from .models import Bio, HttpRequest


class BioAdmin(admin.ModelAdmin):
    pass


class HttpRequestAdmin(admin.ModelAdmin):
    pass


admin.site.register(Bio, BioAdmin)
admin.site.register(HttpRequest, HttpRequestAdmin)
