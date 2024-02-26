from django.contrib import admin
from api.models import Kiosk
from django.contrib import admin,messages

@admin.register(Kiosk)
class KioskAdmin(admin.ModelAdmin):    
     list_display= ("nom", "addresse", "contact","NIF","RC",)
     search_fields = ("nom","addresse",)
     #search_fields = "profile__telephone","attribution","profile__user__first_name",
     #list_filter = "attribution",
     list_filter = ("nom","addresse",)
     def delete_model(self, request, obj:Kiosk):
        nom = obj.nom
        nom.save()
        obj.delete()
        self.message_user(request, "vyahanaguritse neza cane", messages.SUCCESS)
    
     def delete_queryset(self, request, queryset):
        for kiosk in queryset:
            nom = kiosk.nom
            nom.save()
            kiosk.delete()
            self.message_user(request, "vyahanaguritse neza cane", messages.SUCCESS)

