from typing import Any
from django.contrib import admin,messages
from .models import *
from django.utils.safestring import mark_safe
from django.db import transaction
from admin_totals.admin import ModelAdminTotals
from import_export.admin import ImportExportModelAdmin
from .ressources import ProduitResource

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
     list_display= "user", "telephone"
     search_fields="user__first__name","user__last__name",
     list_filter = "user",
  

@admin.register(Kiosk)
class KioskAdmin(admin.ModelAdmin):    
     list_display= "nom", "addresse", "contact","NIF","RC",
     search_fields = "nom","addresse",
     #search_fields = "profile__telephone","attribution","profile__user__first_name",
     #list_filter = "attribution",
     list_filter = "nom","addresse",

@admin.register(Attribution)
class AttributionAdmin(admin.ModelAdmin):
         list_display = "profile","attribution","kiosk",
         search_fields = "attribution","profile__user__first_name","profile__user__last_name","kiosk__nom","profile__telephone"
         list_filter=  "attribution",

@admin.register(Produit)
class ProduitAdmin(ImportExportModelAdmin,admin.ModelAdmin):
     list_display = "nom","kiosk" ,"prix","quantite","ventes","pertes"    
     search_fields= "nom","kiosk__nom",
     list_filter = "nom","kiosk__nom","prix",
     list_editable ="prix",
     actions = "vendre","perdue","augmenter_stock"
     resource_class = ProduitResource

     def ventes(self, obj:Vente):
        return mark_safe(f"<a href='/admin/api/vente/?vente__id={obj.id}'>vente</a>")

     def pertes(self, obj:Perte):
         return mark_safe(f"<a href='/admin/api/perte/?perte__id={obj.id}'>perte</a>")
     @transaction.atomic
     def vendre (self,request,queryset:list[Produit]):
        user = request.user
        profile:Profile =user.profile
        commande= Commande(vendeur = profile )
        commande.save()
        for produit in queryset:
            vente = Vente(produit=produit,commande=commande,quantite=1)
            commande.prix_total += produit.prix
            produit.quantite -=1
            vente.save()
            produit.save()
        commande.save()
        self.message_user (request,f"la commande valant {commande.prix_total} a ete soumise",messages.SUCCESS)
     vendre.short_description="dandaza izi produits"

     @transaction.atomic
     def perdue(self, request, queryset):
        user = request.user  
        for produit in queryset:
                perte = Perte.objects.create(produit=produit, quantite=produit.quantite, user=user)
                produit.quantite -= 1
                produit.save()
                messages.success(request, f"{produit.nom} a été marqué comme perdu.")
     perdue.short_description = "Marquer comme perdu"


     @transaction.atomic
     def augmenter_stock(self, request, queryset):
        for produit in queryset:
            produit.quantite += 5 
            produit.save()
            stock = Stock.objects.get(produit=produit)
            stock.quantite += 5
            stock.save()
            messages.success(request, "5 unités ont été ajoutées à chaque produit sélectionné et stock.", messages.SUCCESS)


     def get_queryset(self,request):
           user = request.user
           if Profile.objects.filter(user=user).exists():
             profile = user.profile
             kiosks =[]
             for attribution in Attribution.objects.filter(profile=profile):
                 kiosks.append(attribution.kiosk)
             Produit.objects.filter(kiosk__in=kiosks)
             return  Produit.objects.all()
           #  attributions = Attribution.objects.filter()
           self.message_user(request,"nta profile ufise nta na kimwe wobona!",messages.ERROR)
           return Produit.objects.none()
   
    #  def augmenter_stock(self,request,queryset:list[Produit]):
    #      user = request.user
    #      profile:Profile = user.profile
    #      for produit in queryset:
    #          stock = Stock.objects.get_or_create(profile = profile,produit = produit,quantite = 5)
    #          stock.quantite +=5
    #          produit.quantite += stock.quantite
    #          stock.save()
    #          produit.save()
    #  augmenter_stock.short_description = "kwongeramwo muri stock"

     
@admin.register(Stock)
class StockAdmin(admin.ModelAdmin):
     list_display= "produit","quantite","expiration","profile","created_at",
     search_fields= "produit","created_at","expiration",
     list_filter = "produit","expiration",

     def save_model(self, request, obj:Stock, form, change) :
           profile = request.user.profile
           if not change:
                produit = obj.produit
                produit.quantite += obj.quantite
                produit.save()
           obj.profile = profile
           obj.save()


     def delete_model(self, request, obj:Stock):
        produit = obj.produit
        produit.quantite += obj.quantite
        produit.save()
        obj.delete()
        self.message_user(request, "vyahanaguritse neza cane", messages.SUCCESS)
    
     def delete_queryset(self, request, queryset):
        for stock in queryset:
            produit = stock.produit
            produit.quantite += stock.quantite
            produit.save()
            stock.delete()
            self.message_user(request, "vyahanaguritse neza cane", messages.SUCCESS)

    
#quantite = quantite_se_trouvant_dans_le_stock -quantite_vendue-quantite_perdue     

@admin.register(Etagere)
class EtagereAdmin(admin.ModelAdmin):
     list_display= "produit","quantite",
     search_fields="produit","quantite",
     list_filter = "emplacement",
     
@admin.register(Vente)
class VenteAdmin(admin.ModelAdmin):
      list_display= "produit","quantite","commande",
      search_fields = "produit","quantite",
      list_filter = "produit","quantite","commande"

      def save_model(self, request, obj:Stock, form, change):
        if not change :
             produit = obj.produit
             produit.quantite -= obj.quantite
             produit.save()
        obj.user = request.user
        obj.save()

      def delete_model(self, request, obj:Vente):
        produit = obj.produit
        produit.quantite += obj.quantite
        produit.save()
        obj.delete()
        self.message_user(request, "vyahanaguritse neza cane", messages.SUCCESS)
    
      def delete_queryset(self, request, queryset):
        for vente in queryset:
            produit = vente.produit
            produit.quantite += vente.quantite
            produit.save()
            vente.delete()
            self.message_user(request, "vyahanaguritse neza cane", messages.SUCCESS)
 

@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
      list_display= "nom","telephone","nif",
      search_fields = "nom","telephone",
      list_filter = "nom",

#je veux que a chaque fois je fais un paiement, il vient s'ajouter dans la partie get_montant.donc dans montant_paye sera montre la sommation de toutes les paiements deja effectue
             

@admin.register(Commande)
class CommandeAdmin(ModelAdminTotals):
    list_display = ['vendeur', 'date', 'prix_total', 'client','montant_paye','produits']
    list_filter = 'date',
    search_fields = 'vendeur__user__first_name', 'vendeur__user__last_name',
    readonly_fields = ['prix_total','montant_paye']
    #list_totals =("prix_total" ,models.sum)

    def save_model(self, request, obj, form, change):
        vendeur = request.user.profile
        obj.vendeur = vendeur
        obj.save()

    def prix_total(self, obj):
        total = sum(vente.produit.prix * vente.quantite for vente in obj.vente_set.all())
        return total
    prix_total.short_description = 'Prix Total'

    def delete_model(self, request, obj:Commande):
        produit = obj.produit
        produit.quantite += obj.quantite
        produit.save()
        self.delete()
        self.message_user(request, "vyahanaguritse neza cane", messages.SUCCESS)
    
    def delete_queryset(self, request, queryset):
        for commande in queryset:
            produit = commande.produit
            produit.quantite += commande.quantite
            produit.save()
            commande.delete()
            self.message_user(request, "vyahanaguritse neza cane", messages.SUCCESS)

    def montant_paye(self, obj):
        payments = Payment.objects.filter(commande=obj)
        total_paid = sum(payment.somme for payment in payments)
        return total_paid
    
    def produits(self, obj:Commande):
        return mark_safe(f"<a href='/admin/api/vente/?commande__id={obj.id}'>produits</a>")
        
    #montant_paye.short_description = 'Montant Payé'


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
      list_display= "commande","somme","date","receveur",
      search_fields = "commande","receveur",
      list_filter = "commande","date","receveur",
 
          
@admin.register(Perte)
class PerteAdmin(admin.ModelAdmin):
      list_display= "produit","quantite","motif","date",
      search_fields = "produit","motif","quantite",
      list_filter = "date",


      def save_model(self, request, obj:Stock, form, change):
        if not change :
             produit = obj.produit
             produit.quantite -= obj.quantite
            #  produit.quantite = models.F("quantite")-obj.quantite
            #  produit.refresh_from_db()
             produit.save()
        obj.user = request.user
        obj.save()

      def delete_model(self, request, obj:Perte):
        produit = obj.produit
        produit.quantite += obj.quantite
        produit.save()
        obj.delete()
        self.message_user(request, "vyahanaguritse neza cane", messages.SUCCESS)
    
      def delete_queryset(self, request, queryset):
        for perte in queryset:
            produit = perte.produit
            produit.quantite += perte.quantite
            produit.save()
            perte.delete()
            self.message_user(request, "vyahanaguritse neza cane", messages.SUCCESS)

    
 
     















