from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    telephone = models.CharField(max_length=16)

class Kiosk(models.Model):
    id = models.AutoField(primary_key=True)
    nom = models.CharField(max_length=64)
    addresse =models.CharField(max_length=64)
    NIF = models.CharField(max_length=32 ,null=True,blank=True)
    RC = models.CharField(max_length=16 ,null=True,blank=True)
    contact =models.CharField(max_length=64,null=True,blank=True)

class Attribution(models.Model):
    id=models.BigAutoField(primary_key=True)
    profile = models.ForeignKey(Profile,on_delete = models.CASCADE)
    kiosk = models.ForeignKey(Kiosk,on_delete = models.CASCADE)
    attribution = models.CharField(max_length=16)

class Produit(models.Model):
    id=models.BigAutoField(primary_key=True)
    nom = models.CharField(max_length=64)
    kiosk = models.ForeignKey(Kiosk,on_delete = models.CASCADE)
    prix = models.FloatField()

class Stock (models.Model):
    id = models.BigAutoField(primary_key=True)
    produit = models.ForeignKey(Produit,on_delete = models.CASCADE)
    quantite = models.FloatField()
    created_at= models.DateTimeField()
    expiration = models.DateTimeField() 
    profile = models.ForeignKey(Profile,on_delete = models.CASCADE)
    date_sortie = models.DateField(auto_now=True)
    prix_achat = models.FloatField()
   
class Etagere(models.Model):
    id = models.BigAutoField(primary_key=True)
    produit = models.ForeignKey(Produit,on_delete = models.CASCADE)
    quantite = models.FloatField()
    emplacement = models.CharField(max_length=64) 

class Vente(models.Model):
    id = models.BigAutoField(primary_key=True)
    produit = models.ForeignKey(Produit,on_delete = models.CASCADE)
    quantite = models.FloatField()
    prix = models.FloatField()
    date_vente = models.DateTimeField(auto_now=True)
    reste = models.FloatField()

class Clients(models.Model):
    id = models.BigAutoField(primary_key=True)
    nom = models.CharField(max_length=64)
    telephone = models.CharField(max_length=16)
    adresse = models.TextField()

class Perte(models.Model):
    id = models.AutoField(primary_key=True)
    produit = models.ForeignKey(Produit,on_delete = models.CASCADE)
    prix = models.FloatField()
    quantite = models.FloatField()
    raison = models.CharField(max_length=100)
    date_perte = models.DateTimeField(auto_now=True)
#donne-moi les models detailles de vente,clients,perte
# class Vente(models.Model):
# class Clients(models.Model):
# class Perte(models.Model):
