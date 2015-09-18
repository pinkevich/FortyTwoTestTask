from django.contrib import admin

from .models import Bio, HttpRequest, History


class BioAdmin(admin.ModelAdmin):
    pass


class HttpRequestAdmin(admin.ModelAdmin):
    pass


class HistoryAdmin(admin.ModelAdmin):
    list_display = ('model_name', 'model_instance', 'action', 'date')
    list_filter = ('action',)


admin.site.register(Bio, BioAdmin)
admin.site.register(HttpRequest, HttpRequestAdmin)
admin.site.register(History, HistoryAdmin)
