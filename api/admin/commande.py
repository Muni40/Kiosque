from django.contrib import admin
from api.models import Commande,Payment,Profile,Attribution
from django.contrib import admin,messages
from django.utils.safestring import mark_safe

@admin.register(Commande)
class CommandeAdmin(admin.ModelAdmin):
    list_display = ['vendeur', 'prix_total', 'client','montant_paye','produits','kiosk']
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
             return Commande.objects.filter(kiosk__in=kiosks)
             #return  Produit.objects.all() # Le queryset filtré des produits est retourné.
           #  attributions = Attribution.objects.filter()
           self.message_user(request,"nta profile ufise nta na kimwe wobona!",messages.ERROR)# Si aucun profil n'est associé à l'utilisateur connecté, un message d'erreur est affiché à l'utilisateur à l'aide de self.message_user(). Dans ce cas, la méthode retourne un queryset vide en utilisant Produit.objects.none().
           return Commande.objects.none()

    def montant_paye(self, obj):
        payments = Payment.objects.filter(commande=obj)
        total_paid = sum(payment.somme for payment in payments)
        return total_paid
    
    def produits(self, obj:Commande):
        return mark_safe(f"<a href='/admin/api/vente/?commande__id={obj.id}'>produits</a>")
        
    #montant_paye.short_description = 'Montant Payé'


