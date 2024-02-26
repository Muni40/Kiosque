from django.contrib import admin
from api.models import Attribution

@admin.register(Attribution)
class AttributionAdmin(admin.ModelAdmin):
         list_display = "profile","attribution","kiosk",
         search_fields = "attribution","profile__user__first_name","profile__user__last_name","kiosk__nom","profile__telephone"
         list_filter=  "attribution",
