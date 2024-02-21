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
        return f"{self.user.last_name}-{self.user.first_name}-{self.telephone}"

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

    def __str__(self) :
        return f"{self.kiosk}-{self.nom}-{self.prix}"

class Stock (models.Model):
    id = models.BigAutoField(primary_key=True)
    produit = models.ForeignKey(Produit,on_delete = models.PROTECT)
    quantite = models.FloatField()
    created_at= models.DateField()
    expiration = models.DateField() 
    profile = models.ForeignKey(Profile,on_delete = models.PROTECT,editable=False)
    prix_achat = models.FloatField()

    def __str__(self) -> str:
        return f"{self.produit}-{self.quantite}-{self.profile}"
   
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
        return f"{self.nom}-{self.telephone}"
    
class Commande(models.Model):
    id = models.BigAutoField(primary_key=True)
    vendeur = models.ForeignKey(Profile,on_delete=models.PROTECT)
    date = models.DateTimeField(auto_now_add=True)
    prix_total =models.FloatField()
    client =models.ForeignKey(Client,null=True,blank=True,on_delete=models.SET_NULL)

    def somme_payee(self):
        total = 0
        payments = Payment.objects.filter(commande=self)
        for payment in payments:
            total += payment.somme
        return total
    #methode qui calcule la somme totale des paiements effectués pour cette commande
    
    def __str__(self):
        return f"{self.vendeur}-{self.date}"

class Vente(models.Model):
    id = models.BigAutoField(primary_key=True)
    produit = models.ForeignKey(Produit,on_delete = models.PROTECT)
    quantite = models.FloatField()
    commande =models.ForeignKey(Commande,on_delete = models.CASCADE)
    prix_total = models.FloatField()

    def __str__(self) :
        return f"{self.produit}-{self.quantite}-{self.commande}"

class Payment(models.Model):
    id = models.BigAutoField(primary_key=True)
    commande = models.ForeignKey(Commande,on_delete=models.PROTECT)
    somme = models.FloatField()
    receveur =models.ForeignKey(Profile, on_delete=models.PROTECT)
    date =models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.commande}-{self.somme}"

   
class Perte(models.Model):
    id = models.AutoField(primary_key=True)
    produit = models.ForeignKey(Produit,null = True ,on_delete = models.SET_NULL)
    quantite = models.FloatField()
    motif = models.CharField(max_length=256)
    date = models.DateTimeField()

    def __str__(self):
        return f"{self.produit}-{self.quantite}"
