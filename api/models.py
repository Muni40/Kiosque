from django.db import models
from django.contrib.auth.models import User

class ATTRIBUTION(models.TextChoices):
    GERANT = "gerant"
    VENDEUR = "vendeur"
    STOCK_MANAGER = "stock manager"

class Profile(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.OneToOneField(User,on_delete=models.CASCADE)#lorsque l'utilisateur est supprimé, le profil correspondant sera également supprimé. Cela garantit l'intégrité référentielle de la base de données. C'est-à-dire que si un utilisateur est supprimé, son profil sera également supprimé pour éviter les incohérences dans les données.
    telephone = models.CharField(max_length=16)

    class Meta:
        ordering = "user", 
        verbose_name_plural ="Profiles"

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name} {self.telephone}"

class Kiosk(models.Model):
    id = models.AutoField(primary_key=True)
    nom = models.CharField(max_length=64)
    addresse =models.CharField(max_length=64)
    NIF = models.CharField(max_length=32 ,null=True,blank=True)
    RC = models.CharField(max_length=16 ,null=True,blank=True)
    contact =models.CharField(max_length=64,null=True,blank=True)

    class Meta:
        ordering = "nom",
        verbose_name_plural ="Kiosks"

    def __str__(self):
        return f"{self.nom}"

class Attribution(models.Model):
    id=models.BigAutoField(primary_key=True)
    profile = models.ForeignKey(Profile,on_delete = models.CASCADE)
    kiosk = models.ForeignKey(Kiosk,on_delete = models.CASCADE)
    attribution = models.CharField(max_length=16 ,choices=ATTRIBUTION.choices)

    class Meta:
        ordering = "profile",
        verbose_name_plural ="Attributions"

    def __str__(self):
        return f"{self.attribution}"

class Produit(models.Model):
    id=models.BigAutoField(primary_key=True)
    nom = models.CharField(max_length=64)
    kiosk = models.ForeignKey(Kiosk,on_delete = models.CASCADE)
    prix = models.FloatField()
    quantite = models.FloatField(default=0,editable=False)
    
    class Meta:
        ordering = "quantite",#Indique que les instances de ce modèle doivent être triées en fonction de la quantité du produit par défaut.
        verbose_name_plural ="Produits"# Définit le nom pluriel utilisé pour ce modèle dans l'interface d'administration Django.
        unique_together ="nom","kiosk", # Cela signifie qu'un produit ne peut pas être ajouté deux fois au même kiosque avec le même nom.  
        constraints= [
            models.CheckConstraint(
                check=models.Q(quantite__gte=0),
                name="quantite ntishobora kuba negative"),
                models.CheckConstraint(
                    check=models.Q(prix__gte=100),
                    name="prix ntishobora kuba negative"),
                 ]
        # Définit des contraintes sur les champs du modèle. Dans ce cas, deux contraintes sont définies : une pour s'assurer que la quantité du produit ne peut pas être négative et une autre pour s'assurer que le prix du produit est supérieur ou égal à 100.

    # def quantite(self):
    #     en_stock= vendue= perdue=0
    #     ventes = Vente.objects.filter(produit =self)
    #     stocks = Stock.objects.filter(produit =self)
    #     pertes = Perte.objects.filter(produit =self)
    #     for perte in pertes:
    #         perdue += perte.quantite
    #     for vente in ventes:
    #         vendue += vente.quantite
    #     for stock in stocks:
    #         en_stock = stock.quantite
    #         return en_stock-(vendue+perdue)

    #0n peut creer une fonction ici et une autre dans admin ou creer un 
    def __str__(self) :
        return f"{self.kiosk} {self.nom} a {self.prix} BIF"

class Stock (models.Model):
    id = models.BigAutoField(primary_key=True)
    produit = models.ForeignKey(Produit,on_delete = models.PROTECT)
    quantite = models.FloatField()
    created_at= models.DateField()
    expiration = models.DateField() 
    profile = models.ForeignKey(Profile,on_delete = models.PROTECT,editable=False)# ce qui signifie que si le profil utilisateur auquel ce stock est associé est supprimé, cela lèvera une exception ProtectedError. Cela protège le stock en cas de suppression accidentelle du profil utilisateur.
    prix_achat = models.FloatField()
    kiosk = models.ForeignKey(Kiosk, on_delete=models.PROTECT)

    class Meta:
        ordering = "quantite",
        verbose_name_plural ="Stocks"
        # constraints= [
        #     models.CheckConstraint(
        #         check=models.Q(quantite__gte=0),
        #         name="quantite ntishobora kuba negative"),
        #         # models.CheckConstraint(
        #         #     check=models.Q(prix_achat__gte=100),
        #         #     name="prix ntishobora kuba negative"),
        #          ]

    def __str__(self) -> str:
        return f"{self.produit.nom} du {self.created_at}"
   
class Etagere(models.Model):
    id = models.BigAutoField(primary_key=True)
    produit = models.ForeignKey(Produit,on_delete = models.CASCADE)
    quantite = models.FloatField()
    emplacement = models.CharField(max_length=64) 

    def __str__(self):
        return f"{self.produit}-{self.quantite}"

class Client(models.Model):
    id = models.BigAutoField(primary_key=True)
    nom = models.CharField(max_length=64)
    telephone = models.CharField(max_length=16)
    nif = models.CharField(max_length=16 ,null=True,blank=True)
    rc = models.CharField(max_length=16 ,null=True,blank=True)
    
    class Meta:
        ordering = "nom",
        verbose_name_plural ="Clients"
    def __str__(self):
        return f"{self.nom} {self.telephone}"
    
class Commande(models.Model):
    id = models.BigAutoField(primary_key=True)
    vendeur = models.ForeignKey(Profile,on_delete=models.PROTECT,editable=False)#ce qui signifie que si le profil du vendeur associé à cette commande est supprimé, cela lèvera une exception ProtectedError. Le champ est également marqué comme non modifiable (editable=False), ce qui signifie qu'il ne peut pas être modifié après la création de la commande.
    date = models.DateTimeField(auto_now_add=True)
    prix_total =models.FloatField(editable=False, default=0)
    client =models.ForeignKey(Client,null=True,blank=True,on_delete=models.SET_NULL)#ce qui signifie que si le client associé à cette commande est supprimé, le champ sera défini sur NULL, ce qui permet de conserver la commande sans client associé. Ce champ peut être nul (null=True) et vide (blank=True).
    kiosk = models.ForeignKey(Kiosk,on_delete =models.CASCADE)
    class Meta:
        ordering = "date",
        verbose_name_plural ="Commandes"
        # constraints= [
        #         models.CheckConstraint(
        #             check=models.Q(prix_total__gte=100),
        #             name="prix ntishobora kuba negative"),
        #          ]
    def somme_payee(self):
        total = 0
        payments = Payment.objects.filter(commande=self)
        for payment in payments:
            total += payment.somme
        return total
    #Cette méthode calcule la somme totale des paiements effectués pour cette commande. Elle récupère tous les paiements associés à cette commande et retourne leur somme totale.
    def __str__(self):
        if self.client:
            return f"{self.client.nom} "
        else:
            return "No client"
# Cette méthode est utilisée pour représenter une instance de ce modèle sous forme de chaîne. Si la commande a un client associé, elle renvoie le nom du client. Sinon, elle renvoie "No client".
    
    # def __str__(self):    
    #     return f"{self.client.nom} " 

class Vente(models.Model):
    id = models.BigAutoField(primary_key=True)
    produit = models.ForeignKey(Produit,on_delete = models.PROTECT)
    quantite = models.FloatField()
    commande =models.ForeignKey(Commande,on_delete = models.CASCADE)
    kiosk = models.ForeignKey(Kiosk,on_delete = models.PROTECT)
    #prix_total = models.FloatField()
    class Meta:
        ordering = "quantite",
        verbose_name_plural ="Ventes"
        # constraints= [
        #     models.CheckConstraint(
        #         check=models.Q(quantite__gte=0),
        #         name="quantite ntishobora kuba negative"),
        #          ]

    def __str__(self) :
        return f"{self.quantite} de {self.produit.nom} "

class Payment(models.Model):
    id = models.BigAutoField(primary_key=True)
    commande = models.ForeignKey(Commande,on_delete=models.PROTECT)
    somme = models.FloatField()
    receveur =models.ForeignKey(Profile, on_delete=models.PROTECT,editable=False)
    date =models.DateTimeField(auto_now_add=True)
    kiosk = models.ForeignKey(Kiosk, on_delete=models.PROTECT)
    class Meta:
        ordering = "date",
        verbose_name_plural ="Payments"

    def __str__(self):
        return f"{self.somme} BIF sur {self.commande} recu par {self.receveur.user.last_name}"

   
class Perte(models.Model):
    id = models.BigAutoField(primary_key=True)
    produit = models.ForeignKey(Produit,null = True ,on_delete = models.SET_NULL)
    user = models.ForeignKey(Profile, on_delete=models.PROTECT,editable=False)
    quantite = models.FloatField()
    motif = models.CharField(max_length=256)
    date = models.DateTimeField(auto_now_add=True)
    kiosk = models.ForeignKey(Kiosk, on_delete=models.PROTECT)

    class Meta:
        ordering = 'quantite',
        verbose_name_plural = "Pertes"

    def __str__(self):
        return f"{self.quantite} de {self.produit}"
