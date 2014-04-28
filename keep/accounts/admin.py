from django.contrib import admin
from keep.accounts.models import ResearcherIP


class ResearcherIPAdmin(admin.ModelAdmin):
    list_display = ('name', 'ip_address')


admin.site.register(ResearcherIP, ResearcherIPAdmin)