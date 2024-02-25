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
     list_display= ("user", "telephone",)
     search_fields=("user__first__name","user__last__name",)
     list_filter =("user"),
  

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
     list_editable ="prix",#Cette configuration indique quels champs peuvent être édités directement depuis la vue liste de l'interface d'administration. Dans cet exemple, le champ prix est défini comme éditable dans la liste.
     actions = "vendre","perdue","augmenter_stock",#: Cette configuration spécifie les actions personnalisées disponibles pour les enregistrements dans la vue liste de l'interface d'administration.
     resource_class = ProduitResource # Cette configuration spécifie la classe de ressource utilisée pour l'import/export de données pour le modèle Produit.

     def ventes(self, obj:Vente):
        return mark_safe(f"<a href='/admin/api/vente/?vente__id={obj.id}'>vente</a>")
        # Ces méthodes permettent de créer des liens vers les vues détaillées des ventes et des pertes associées à chaque produit dans l'interface d'administration.
     def pertes(self, obj:Perte):
         return mark_safe(f"<a href='/admin/api/perte/?perte__id={obj.id}'>perte</a>")
         # Ces méthodes permettent de créer des liens vers les vues détaillées des ventes et des pertes associées à chaque produit dans l'interface d'administration.
     @transaction.atomic
     def vendre (self,request,queryset:list[Produit]):
        user = request.user# L'utilisateur actuellement connecté est récupéré à partir de la requête (request.user)
        profile:Profile =user.profile
        commande= Commande(vendeur = profile )
        commande.save()
        for produit in queryset:#Pour chaque produit sélectionné dans le queryset passé à la méthode vendre, une vente est créée avec les détails du produit et de la commande correspondante. La quantité de produit vendue est déduite de la quantité disponible en stock.
            vente = Vente(produit=produit,commande=commande,quantite=1)
            commande.prix_total += produit.prix #Pour chaque produit sélectionné dans le queryset passé à la méthode vendre, une vente est créée avec les détails du produit et de la commande correspondante. La quantité de produit vendue est déduite de la quantité disponible en stock.
            produit.quantite -=1  # La quantité de produit vendue est déduite de la quantité disponible en stock.
            vente.save()
            produit.save()
        commande.save()
        self.message_user (request,f"la commande valant {commande.prix_total} a ete soumise",messages.SUCCESS)
     vendre.short_description="dandaza izi produits"
     #La méthode vendre dans la classe ProduitAdmin est une action personnalisée qui permet de vendre des produits sélectionnés dans l'interface d'administration


     @transaction.atomic  # Cette méthode est décorée avec @transaction.atomic pour garantir que toutes les opérations de base de données liées à cette action se déroulent dans une transaction, assurant ainsi la cohérence des données.
     def perdue(self, request, queryset):
        user = request.user  
        for produit in queryset:# Pour chaque produit sélectionné dans le queryset passé à la méthode perdue, une nouvelle instance de Perte est créée avec les détails du produit et la quantité totale du produit est enregistrée comme quantité perdue.
                perte = Perte.objects.create(produit=produit, quantite=produit.quantite, user=user)
                produit.quantite -= 1 #la quantité du produit dans le stock est décrémentée de 1 
                produit.save()
                messages.success(request, f"{produit.nom} a été marqué comme perdu.")
     perdue.short_description = "Marquer comme perdu"


     @transaction.atomic
     def augmenter_stock(self, request, queryset):
        for produit in queryset:#Pour chaque produit sélectionné dans le queryset passé à la méthode augmenter_stock, la quantité disponible du produit est augmentée de 5 unités.
            produit.quantite += 5 
            produit.save()
            stock = Stock.objects.get(produit=produit)#Après avoir mis à jour la quantité du produit, la méthode récupère l'objet Stock correspondant à ce produit et met également à jour sa quantité en stock en ajoutant 5 unités.
            stock.quantite += 5
            stock.save()
            messages.success(request, "5 unités ont été ajoutées à chaque produit sélectionné et stock.", messages.SUCCESS)


     def get_queryset(self,request):#Cette méthode get_queryset dans la classe ProduitAdmin est utilisée pour obtenir le queryset des objets Produit qui seront affichés dans l'interface d'administration
           user = request.user
           if Profile.objects.filter(user=user).exists(): # On vérifie si un profil utilisateur est associé à l'utilisateur connecté. Cela se fait en vérifiant si un objet Profile existe pour cet utilisateur dans la base de données.
             profile = user.profile
             kiosks =[]
             for attribution in Attribution.objects.filter(profile=profile): #Si un profil utilisateur existe, on récupère tous les kiosques associés à ce profil à travers les objets Attribution. On boucle à travers les attributions pour ce profil et on ajoute les kiosques correspondants à une liste kiosks.
                 kiosks.append(attribution.kiosk) 
             #Produit.objects.filter(kiosk__in=kiosks)#On filtre les produits pour ne sélectionner que ceux qui sont associés aux kiosques récupérés dans l'étape précédente. Cela est réalisé en utilisant la méthode filter() avec l'argument kiosk__in=kiosks.
             return Produit.objects.filter(kiosk__in=kiosks)
             #return  Produit.objects.all() # Le queryset filtré des produits est retourné.
           #  attributions = Attribution.objects.filter()
           self.message_user(request,"nta profile ufise nta na kimwe wobona!",messages.ERROR)# Si aucun profil n'est associé à l'utilisateur connecté, un message d'erreur est affiché à l'utilisateur à l'aide de self.message_user(). Dans ce cas, la méthode retourne un queryset vide en utilisant Produit.objects.none().
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
            
     def delete_model(self, request, obj:Produit):
        nom = obj.nom
        nom.save()
        obj.delete()
        self.message_user(request, "vyahanaguritse neza cane", messages.SUCCESS)
    
     def delete_queryset(self, request, queryset):
        for produit in queryset:
            nom = produit.nom
            nom.save()
            produit.delete()
            self.message_user(request, "vyahanaguritse neza cane", messages.SUCCESS)

     
@admin.register(Stock)
class StockAdmin(admin.ModelAdmin):
     list_display= "produit","quantite","expiration","profile","created_at",
     search_fields= "produit","created_at","expiration",
     list_filter = "produit","expiration",

     def save_model(self, request, obj:Stock, form, change) :#: La méthode save_model est une méthode de ModelAdmin qui est appelée chaque fois qu'un modèle est sauvegardé via l'interface d'administration.
           profile = request.user.profile
           if not change:
                produit = obj.produit
                produit.quantite += obj.quantite # Si l'instance de Stock est nouvellement créée (c'est-à-dire qu'elle n'a pas encore été sauvegardée dans la base de données), la méthode vérifie si l'attribut change est False. Si c'est le cas, cela signifie qu'il s'agit d'une nouvelle instance.
                produit.save()
           obj.profile = profile #le profil de l'utilisateur est associé à l'objet Stock et l'objet Stock est sauvegardé dans la base de données.
           obj.save()


     def delete_model(self, request, obj:Stock): #Cette méthode delete_model dans la classe StockAdmin est utilisée pour personnaliser le processus de suppression d'un objet Stock via l'interface d'administration Django.
        produit = obj.produit
        produit.quantite += obj.quantite
        produit.save()
        obj.delete()
        self.message_user(request, "vyahanaguritse neza cane", messages.SUCCESS)
    
     def delete_queryset(self, request, queryset): #Cette méthode delete_queryset dans la classe StockAdmin est utilisée pour personnaliser le processus de suppression de plusieurs objets Stock via l'interface d'administration Django. 
        for stock in queryset:
            produit = stock.produit
            produit.quantite += stock.quantite
            produit.save()
            stock.delete()
            self.message_user(request, "vyahanaguritse neza cane", messages.SUCCESS)

     def get_queryset(self,request):#Cette méthode get_queryset dans la classe ProduitAdmin est utilisée pour obtenir le queryset des objets Produit qui seront affichés dans l'interface d'administration
           user = request.user
           if Profile.objects.filter(user=user).exists(): # On vérifie si un profil utilisateur est associé à l'utilisateur connecté. Cela se fait en vérifiant si un objet Profile existe pour cet utilisateur dans la base de données.
             profile = user.profile
             kiosks =[]
             for attribution in Attribution.objects.filter(profile=profile): #Si un profil utilisateur existe, on récupère tous les kiosques associés à ce profil à travers les objets Attribution. On boucle à travers les attributions pour ce profil et on ajoute les kiosques correspondants à une liste kiosks.
                 kiosks.append(attribution.kiosk) 
             #Produit.objects.filter(kiosk__in=kiosks)#On filtre les produits pour ne sélectionner que ceux qui sont associés aux kiosques récupérés dans l'étape précédente. Cela est réalisé en utilisant la méthode filter() avec l'argument kiosk__in=kiosks.
             return Produit.objects.filter(kiosk__in=kiosks)
             #return  Produit.objects.all() # Le queryset filtré des produits est retourné.
           #  attributions = Attribution.objects.filter()
           self.message_user(request,"nta profile ufise nta na kimwe wobona!",messages.ERROR)# Si aucun profil n'est associé à l'utilisateur connecté, un message d'erreur est affiché à l'utilisateur à l'aide de self.message_user(). Dans ce cas, la méthode retourne un queryset vide en utilisant Produit.objects.none().
           return Produit.objects.none()

    
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

      def get_queryset(self,request):#Cette méthode get_queryset dans la classe ProduitAdmin est utilisée pour obtenir le queryset des objets Produit qui seront affichés dans l'interface d'administration
           user = request.user
           if Profile.objects.filter(user=user).exists(): # On vérifie si un profil utilisateur est associé à l'utilisateur connecté. Cela se fait en vérifiant si un objet Profile existe pour cet utilisateur dans la base de données.
             profile = user.profile
             kiosks =[]
             for attribution in Attribution.objects.filter(profile=profile): #Si un profil utilisateur existe, on récupère tous les kiosques associés à ce profil à travers les objets Attribution. On boucle à travers les attributions pour ce profil et on ajoute les kiosques correspondants à une liste kiosks.
                 kiosks.append(attribution.kiosk) 
             #Produit.objects.filter(kiosk__in=kiosks)#On filtre les produits pour ne sélectionner que ceux qui sont associés aux kiosques récupérés dans l'étape précédente. Cela est réalisé en utilisant la méthode filter() avec l'argument kiosk__in=kiosks.
             return Produit.objects.filter(kiosk__in=kiosks)
             #return  Produit.objects.all() # Le queryset filtré des produits est retourné.
           #  attributions = Attribution.objects.filter()
           self.message_user(request,"nta profile ufise nta na kimwe wobona!",messages.ERROR)# Si aucun profil n'est associé à l'utilisateur connecté, un message d'erreur est affiché à l'utilisateur à l'aide de self.message_user(). Dans ce cas, la méthode retourne un queryset vide en utilisant Produit.objects.none().
           return Produit.objects.none()
 

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




        #je veux que a chaque fois je fais un paiement, il vient s'ajouter dans la partie get_montant.donc dans montant_paye sera montre la sommation de toutes les paiements deja effectue
             

@admin.register(Commande)
class CommandeAdmin(admin.ModelAdmin):
    list_display = ['vendeur', 'prix_total', 'client','montant_paye','produits']
    list_filter = 'date',
    search_fields = 'vendeur__user__first_name', 'vendeur__user__last_name',
    readonly_fields = ['prix_total','montant_paye']# Cette configuration spécifie les champs qui sont en lecture seule dans l'interface d'administration.
    #list_totals =("prix_total" ,models.sum)

    def save_model(self, request, obj, form, change): #Cette méthode est appelée chaque fois qu'un modèle est sauvegardé via l'interface d'administration. Elle récupère le vendeur à partir de l'utilisateur actuellement connecté et l'associe à la commande avant de sauvegarder.
        vendeur = request.user.profile
        obj.vendeur = vendeur
        obj.save()

    def prix_total(self, obj): #Cette méthode calcule le prix total de la commande en récupérant toutes les ventes associées à la commande et en calculant la somme des prix des produits vendus multipliés par leur quantité.
        total = sum(vente.produit.prix * vente.quantite for vente in obj.vente_set.all())
        return total
    prix_total.short_description = 'Prix Total'

    # def delete_model(self, request, obj:Commande):
    #     produit = obj.produit
    #     produit.quantite += obj.quantite
    #     produit.save()
    #     self.delete()
    #     self.message_user(request, "vyahanaguritse neza cane", messages.SUCCESS)
    
    # def delete_queryset(self, request, queryset):
    #     for commande in queryset:
    #         produit = commande.produit
    #         produit.quantite += commande.quantite
    #         produit.save()
    #         commande.delete()
    #         self.message_user(request, "vyahanaguritse neza cane", messages.SUCCESS)

    def get_queryset(self,request):#Cette méthode get_queryset dans la classe ProduitAdmin est utilisée pour obtenir le queryset des objets Produit qui seront affichés dans l'interface d'administration
           user = request.user
           if Profile.objects.filter(user=user).exists(): # On vérifie si un profil utilisateur est associé à l'utilisateur connecté. Cela se fait en vérifiant si un objet Profile existe pour cet utilisateur dans la base de données.
             profile = user.profile
             kiosks =[]
             for attribution in Attribution.objects.filter(profile=profile): #Si un profil utilisateur existe, on récupère tous les kiosques associés à ce profil à travers les objets Attribution. On boucle à travers les attributions pour ce profil et on ajoute les kiosques correspondants à une liste kiosks.
                 kiosks.append(attribution.kiosk) 
             #Produit.objects.filter(kiosk__in=kiosks)#On filtre les produits pour ne sélectionner que ceux qui sont associés aux kiosques récupérés dans l'étape précédente. Cela est réalisé en utilisant la méthode filter() avec l'argument kiosk__in=kiosks.
             return Produit.objects.filter(kiosk__in=kiosks)
             #return  Produit.objects.all() # Le queryset filtré des produits est retourné.
           #  attributions = Attribution.objects.filter()
           self.message_user(request,"nta profile ufise nta na kimwe wobona!",messages.ERROR)# Si aucun profil n'est associé à l'utilisateur connecté, un message d'erreur est affiché à l'utilisateur à l'aide de self.message_user(). Dans ce cas, la méthode retourne un queryset vide en utilisant Produit.objects.none().
           return Produit.objects.none()

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

      def save_model(self, request, obj, form, change): #Cette méthode est appelée chaque fois qu'un modèle est sauvegardé via l'interface d'administration. Elle récupère le vendeur à partir de l'utilisateur actuellement connecté et l'associe à la commande avant de sauvegarder.
        receveur = request.user.profile
        obj.receveur = receveur
        obj.save()

      def get_queryset(self,request):#Cette méthode get_queryset dans la classe ProduitAdmin est utilisée pour obtenir le queryset des objets Produit qui seront affichés dans l'interface d'administration
           user = request.user
           if Profile.objects.filter(user=user).exists(): # On vérifie si un profil utilisateur est associé à l'utilisateur connecté. Cela se fait en vérifiant si un objet Profile existe pour cet utilisateur dans la base de données.
             profile = user.profile
             kiosks =[]
             for attribution in Attribution.objects.filter(profile=profile): #Si un profil utilisateur existe, on récupère tous les kiosques associés à ce profil à travers les objets Attribution. On boucle à travers les attributions pour ce profil et on ajoute les kiosques correspondants à une liste kiosks.
                 kiosks.append(attribution.kiosk) 
             #Produit.objects.filter(kiosk__in=kiosks)#On filtre les produits pour ne sélectionner que ceux qui sont associés aux kiosques récupérés dans l'étape précédente. Cela est réalisé en utilisant la méthode filter() avec l'argument kiosk__in=kiosks.
             return Produit.objects.filter(kiosk__in=kiosks)
             #return  Produit.objects.all() # Le queryset filtré des produits est retourné.
           #  attributions = Attribution.objects.filter()
           self.message_user(request,"nta profile ufise nta na kimwe wobona!",messages.ERROR)# Si aucun profil n'est associé à l'utilisateur connecté, un message d'erreur est affiché à l'utilisateur à l'aide de self.message_user(). Dans ce cas, la méthode retourne un queryset vide en utilisant Produit.objects.none().
           return Produit.objects.none()
 
          
@admin.register(Perte)
class PerteAdmin(admin.ModelAdmin):
      list_display= "produit","quantite","motif","date",
      search_fields = "produit","motif","quantite",
      list_filter = "date",


      def save_model(self, request, obj:Perte, form, change):
        user = request.user.profile
        if not change :
             produit = obj.produit
             produit.quantite -= obj.quantite
            #  produit.quantite = models.F("quantite")-obj.quantite
            #  produit.refresh_from_db()
             produit.save()
        obj.user = user
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

      def get_queryset(self,request):#Cette méthode get_queryset dans la classe ProduitAdmin est utilisée pour obtenir le queryset des objets Produit qui seront affichés dans l'interface d'administration
           user = request.user
           if Profile.objects.filter(user=user).exists(): # On vérifie si un profil utilisateur est associé à l'utilisateur connecté. Cela se fait en vérifiant si un objet Profile existe pour cet utilisateur dans la base de données.
             profile = user.profile
             kiosks =[]
             for attribution in Attribution.objects.filter(profile=profile): #Si un profil utilisateur existe, on récupère tous les kiosques associés à ce profil à travers les objets Attribution. On boucle à travers les attributions pour ce profil et on ajoute les kiosques correspondants à une liste kiosks.
                 kiosks.append(attribution.kiosk) 
             #Produit.objects.filter(kiosk__in=kiosks)#On filtre les produits pour ne sélectionner que ceux qui sont associés aux kiosques récupérés dans l'étape précédente. Cela est réalisé en utilisant la méthode filter() avec l'argument kiosk__in=kiosks.
             return Produit.objects.filter(kiosk__in=kiosks)
             #return  Produit.objects.all() # Le queryset filtré des produits est retourné.
           #  attributions = Attribution.objects.filter()
           self.message_user(request,"nta profile ufise nta na kimwe wobona!",messages.ERROR)# Si aucun profil n'est associé à l'utilisateur connecté, un message d'erreur est affiché à l'utilisateur à l'aide de self.message_user(). Dans ce cas, la méthode retourne un queryset vide en utilisant Produit.objects.none().
           return Produit.objects.none()

    
 
     















