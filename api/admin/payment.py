from django.contrib import admin
from api.models import Payment,Profile,Attribution
from django.contrib import admin,messages

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
      list_display= "commande","somme","date","receveur",'kiosk'
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
             return Payment.objects.filter(kiosk__in=kiosks)
             #return  Produit.objects.all() # Le queryset filtré des produits est retourné.
           #  attributions = Attribution.objects.filter()
           self.message_user(request,"nta profile ufise nta na kimwe wobona!",messages.ERROR)# Si aucun profil n'est associé à l'utilisateur connecté, un message d'erreur est affiché à l'utilisateur à l'aide de self.message_user(). Dans ce cas, la méthode retourne un queryset vide en utilisant Produit.objects.none().
           return Payment.objects.none()
 
