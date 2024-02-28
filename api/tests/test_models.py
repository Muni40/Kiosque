#from rest_framework.test import APITestCase,APIClient
from .test_setup import TestSetUp
from api.models import Profile,Kiosk,Attribution,Produit,Stock,Client,Commande,Vente
from django.contrib.auth.models import User


class TestProfileModel(TestSetUp):
    def test_str_profile(self):
        #creation d'un objet de type profile
        # creation d'un objet de type user
        user = User.objects.create(
             first_name="Laurette",
             last_name="Banderembako",
             username="Muniii",
            password="dede1990"
        )
        profile = Profile.objects.create(telephone ="62449372",user=user)
        self.assertEqual(str(profile), "Laurette Banderembako 62449372")


class TestKioskModel(TestSetUp):
    def test_str_kiosk(self):
        kiosk = Kiosk.objects.create(nom="Homeworld2")
        self.assertEqual(str(kiosk), "Homeworld2")


class TestAttributionModel(TestSetUp):
    def test_str_attribution(self):
        user = User.objects.create(
             first_name="Jean",
             last_name="Laurent",
             username="Muni",
            password="dede1990"
        )
        profile = Profile.objects.create(telephone ="62449372",user=user)
        kiosk = Kiosk.objects.create(nom="Homeworld2")
        attribution = Attribution.objects.create(profile=profile,kiosk=kiosk,attribution="Gerant")
        self.assertEqual(str(attribution), "Gerant")

class TestClientModel(TestSetUp):
    def test_str_client(self):
        client = Client.objects.create(nom = "Sahara",telephone ="+25745332123",nif = "45678789", rc ="345678")
        self.assertEqual(str(client), "Sahara +25745332123")
class TestProduitModel(TestSetUp):
    def test_str_produit(self):
        kiosk = Kiosk.objects.create(nom="Homeworld2")
        produit = Produit.objects.create(nom="Montre",prix="57000" ,kiosk=kiosk)
        self.assertEqual(str(produit), "Homeworld2 Montre a 57000 BIF")

class TestStockModel(TestSetUp):
    def test_str_stock(self):
        user = User.objects.create(
             first_name="Laurette",
             last_name="Banderembako",
             username="Muni",
            password="dede1990"
        )
        profile = Profile.objects.create(telephone ="62449372",user=user)
        kiosk = Kiosk.objects.create(nom="Homeworld2") 
        produit = Produit.objects.create(nom="Montre",prix="57000" ,kiosk=kiosk)
        stock = Stock.objects.create(profile=profile,produit=produit,kiosk=kiosk, created_at ="2024-02-28",prix_achat="4500",expiration="2030-02-28",quantite = "5")
        self.assertEqual(str(stock), "Montre du 2024-02-28")

class TestCommandeModel(TestSetUp):
    def test_str_Commande(self):
        user = User.objects.create(
             first_name="Laure",
             last_name="Banderemba",
             username="sarah",
            password="dede1990"
        )
        profile = Profile.objects.create(telephone ="62449372",user=user)
        client = Client.objects.create(nom= "Sahara",telephone ="+25745332123",nif = "45678789", rc ="345678")
        kiosk = Kiosk.objects.create(nom="Homeworld3") 
      #  produit = Produit.objects.create(nom="Montre",prix="57000",kiosk=kiosk)
        commande = Commande.objects.create(vendeur=profile,kiosk=kiosk, client=client,prix_total="120999",date="2024-02-28")
        self.assertEqual(str(commande), "Sahara ")


class TestVenteModel(TestSetUp):
    def test_get_stock(self):
        user = User.objects.create(
            first_name="Laure",
            last_name="Banderemba",
            username="sara",
            password="dede1990"
        )
        kiosk = Kiosk.objects.create(nom="Homeworld3") 
        produit = Produit.objects.create(nom="Montre", prix="57000", kiosk=kiosk)
        profile = Profile.objects.create(telephone="62449372", user=user)
        client = Client.objects.create(nom="Sahara", telephone="+25745332123", nif="45678789", rc="345678")
        commande = Commande.objects.create(vendeur=profile, kiosk=kiosk, client=client, prix_total="120999", date="2024-02-28")
        vente = Vente.objects.create(produit=produit, commande=commande, kiosk=kiosk, quantite=9)
        self.assertEqual(str(vente), "9 de Montre ")
