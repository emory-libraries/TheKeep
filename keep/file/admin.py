from django.contrib import admin
from keep.file.models import Application


class ApplicationAdmin(admin.ModelAdmin):
    list_display = ('name', 'version')


admin.site.register(Application, ApplicationAdmin)