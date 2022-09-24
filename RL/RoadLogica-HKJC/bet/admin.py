from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from bet.models import (BetOdds)


class BetOddsResource(resources.ModelResource):
    class Meta:
        model = BetOdds


class BetOddsAdmin(ImportExportModelAdmin):
    resource_class = BetOddsResource
    list_display = ('rank_tag', 'date', 'venue', 'raceno', 'number', 'win', 'pla', 'create_date')
    list_filter = ('date', 'raceno')


admin.site.register(BetOdds, BetOddsAdmin)
