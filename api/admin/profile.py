from django.contrib import admin
from api.models import Profile

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
     list_display= ("user", "telephone",)
     search_fields=("user__first__name","user__last__name",)
     list_filter =("user"),