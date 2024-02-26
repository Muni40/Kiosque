from django.contrib import admin
from api.models import Stock,Profile,Attribution
from django.contrib import admin,messages

@admin.register(Stock)
class StockAdmin(admin.ModelAdmin):
     list_display= "produit","quantite","expiration","profile","created_at",'kiosk',
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
             return Stock.objects.filter(kiosk__in=kiosks)
             #return  Produit.objects.all() # Le queryset filtré des produits est retourné.
           #  attributions = Attribution.objects.filter()
           self.message_user(request,"nta profile ufise nta na kimwe wobona!",messages.ERROR)# Si aucun profil n'est associé à l'utilisateur connecté, un message d'erreur est affiché à l'utilisateur à l'aide de self.message_user(). Dans ce cas, la méthode retourne un queryset vide en utilisant Produit.objects.none().
           return Stock.objects.none()

    