from django.db import models
from django.contrib.auth.models import User

class ATTRIBUTION(models.TextChoices):
    GERANT = "gerant"
    VENDEUR = "vendeur"
    STOCK_MANAGER = "stock manager"

class Profile(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    telephone = models.CharField(max_length=16)

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name} {self.telephone}"

class Kiosk(models.Model):
    id = models.AutoField(primary_key=True)
    nom = models.CharField(max_length=64)
    addresse =models.CharField(max_length=64)
    NIF = models.CharField(max_length=32 ,null=True,blank=True)
    RC = models.CharField(max_length=16 ,null=True,blank=True)
    contact =models.CharField(max_length=64,null=True,blank=True)

    def __str__(self):
        return f"{self.nom}"

class Attribution(models.Model):
    id=models.BigAutoField(primary_key=True)
    profile = models.ForeignKey(Profile,on_delete = models.CASCADE)
    kiosk = models.ForeignKey(Kiosk,on_delete = models.CASCADE)
    attribution = models.CharField(max_length=16 ,choices=ATTRIBUTION.choices)

    def __str__(self):
        return f"{self.attribution}"

class Produit(models.Model):
    id=models.BigAutoField(primary_key=True)
    nom = models.CharField(max_length=64)
    kiosk = models.ForeignKey(Kiosk,on_delete = models.CASCADE)
    prix = models.FloatField()
    quantite = models.FloatField(default=0)

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
    profile = models.ForeignKey(Profile,on_delete = models.PROTECT,editable=False)
    prix_achat = models.FloatField()

    def __str__(self) -> str:
        return f"{self.produit} du {self.created_at}"
   
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
    
    def __str__(self):
        return f"{self.nom} {self.telephone}"
    
class Commande(models.Model):
    id = models.BigAutoField(primary_key=True)
    vendeur = models.ForeignKey(Profile,on_delete=models.PROTECT,editable=False)
    date = models.DateTimeField(auto_now_add=True)
    prix_total =models.FloatField(editable=False, default=0)
    client =models.ForeignKey(Client,null=True,blank=True,on_delete=models.SET_NULL)

    def somme_payee(self):
        total = 0
        payments = Payment.objects.filter(commande=self)
        for payment in payments:
            total += payment.somme
        return total
    def __str__(self):
        if self.client:
            return f"{self.client.nom} "
        else:
            return "No client"

    #methode qui calcule la somme totale des paiements effectués pour cette commande
    
    # def __str__(self):    
    #     return f"{self.client.nom} " 

class Vente(models.Model):
    id = models.BigAutoField(primary_key=True)
    produit = models.ForeignKey(Produit,on_delete = models.PROTECT)
    quantite = models.FloatField()
    commande =models.ForeignKey(Commande,on_delete = models.CASCADE)
    #prix_total = models.FloatField()

    def __str__(self) :
        return f"{self.quantite} de {self.produit} "

class Payment(models.Model):
    id = models.BigAutoField(primary_key=True)
    commande = models.ForeignKey(Commande,on_delete=models.PROTECT)
    somme = models.FloatField()
    receveur =models.ForeignKey(Profile, on_delete=models.PROTECT)
    date =models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.somme} BIF sur {self.commande} recu par {self.receveur.user.last_name}"

   
class Perte(models.Model):
    id = models.BigAutoField(primary_key=True)
    produit = models.ForeignKey(Produit,null = True ,on_delete = models.SET_NULL)
    user = models.ForeignKey(User, on_delete=models.PROTECT,editable=False)
    quantite = models.FloatField()
    motif = models.CharField(max_length=256)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.quantite} de {self.produit}"
