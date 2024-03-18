
from django.contrib import admin
from api.models import Produit,Vente,Perte,Stock,Profile,Attribution,Commande
from django.contrib import admin,messages
# from admin_totals.admin import ModelAdminTotals
from import_export.admin import ImportExportModelAdmin
from ..ressources import ProduitResource
from django.utils.safestring import mark_safe
from django.db import transaction

@admin.register(Produit)
class ProduitAdmin(ImportExportModelAdmin,admin.ModelAdmin):
     list_display = "nom","kiosk" ,"prix","quantite","ventes","pertes" ,   
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

     