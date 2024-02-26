from django.contrib import admin
from api.models import Client,Perte
from django.contrib import admin,messages

@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
      list_display= "nom","telephone","nif",
      search_fields = "nom","telephone",
      list_filter = "nom",
      def delete_model(self, request, obj:Perte):
        nom = obj.nom
        nom.save()
        obj.delete()
        self.message_user(request, "vyahanaguritse neza cane", messages.SUCCESS)
    
      def delete_queryset(self, request, queryset):
        for client in queryset:
            nom = client.nom
            nom.save()
            client.delete()
            self.message_user(request, "vyahanaguritse neza cane", messages.SUCCESS)


