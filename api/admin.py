from typing import Any
from django.contrib import admin
from .models import *


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
     list_display= "user", "telephone"
     search_fields="user__first__name","user__last__name",
     list_filter = "user",
  

@admin.register(Kiosk)
class KioskAdmin(admin.ModelAdmin):    
     list_display= "nom", "addresse", "contact"
     search_fields = "nom","addresse",
     #search_fields = "profile__telephone","attribution","profile__user__first_name",
     #list_filter = "attribution",
     list_filter = "nom","addresse",

@admin.register(Attribution)
class AttributionAdmin(admin.ModelAdmin):
         list_display = "profile","attribution","kiosk",
         search_fields = "attribution","profile__user__first_name","profile__user__last_name","kiosk__nom",
         list_filter=  "attribution","profile__user__first_name","profile__user__last_name","kiosk__nom",

@admin.register(Produit)
class ProduitAdmin(admin.ModelAdmin):
     list_display = "nom","kiosk" ,"prix"
     search_fields= "nom","kiosk__nom",
     list_filter = "nom","kiosk__nom","prix",

@admin.register(Stock)
class StockAdmin(admin.ModelAdmin):
     list_display= "produit","quantite","expiration","profile"
     search_fields= "produit","created_at","expiration",
     list_filter = "produit","expiration",

     def save_model(self, request, obj, form, change) -> None:
           
           if not change:
                profile = request.user.profile
                obj.profile = profile
           obj.save()
      

@admin.register(Etagere)
class EtagereAdmin(admin.ModelAdmin):
     list_display= "produit","quantite",
     search_fields="produit","quantite",
     list_filter = "emplacement",
     
@admin.register(Vente)
class VenteAdmin(admin.ModelAdmin):
      list_display= "produit","quantite","commande"
      search_fields = "produit","quantite",
      list_filter = "produit","quantite",

@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
      list_display= "nom","telephone","nif",
      search_fields = "nom","telephone",
      list_filter = "nom",

#@admin.register(Commande)
# class CommandeAdmin(admin.ModelAdmin):
#      list_display= "vendeur","date",
#      search_fields = "vendeur","client",
#      list_filter = "vendeur","date",
@admin.register(Commande)
class CommandeAdmin(admin.ModelAdmin):
    list_display = ['get_vendeur_attributs', 'date', 'prix_total']
    search_fields = ['vendeur__user__first_name', 'vendeur__user__last_name']
    readonly_fields = ['prix_total']

    def get_vendeur_attributs(self,obj):
         return f"{obj.vendeur__user.first_name} {obj.vendeur.user.last_name} {obj.vendeur.telephone}"

    def prix_total(self):
        total = sum(vente.prix_total for vente in self.vente_set.all())
        return total

     
@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
      list_display= "commande","somme","date","receveur",
      search_fields = "commande","receveur",
      list_filter = "commande","date","receveur",
      
     
@admin.register(Perte)
class PerteAdmin(admin.ModelAdmin):
      list_display= "produit","quantite","motif",
      search_fields = "produit","motif","quantite",
      list_filter = "produit","quantite","date"
 
     















     
# admin.register(History)


# @admin.register(Province)
# class ProvinceAdmin(admin.ModelAdmin):
#     display_fields = "nom",
