from api.models import Kiosk,Profile,Produit,Client
from django.contrib.auth.models import User

profiles = [
    {
        "id": 2,
        "telephone": "62449372",
        "user": {
            "username": "chany",
            "password": "dede1990",
            "first_name": "chany",
            "last_name": "Irakoze",
        }
    },
    {
        "id": 3,
        "telephone": "61449372",
        "user": {
            "username": "Bertilla",
            "password": "dede1990",
            "first_name": "Bertilla",
            "last_name": "Irakoze",
        }
    }
]


def prepopulateProfiles():
    for profile in profiles:
        user = User.objects.create(
            username=profile["user"]["username"],
            password=profile["user"]["password"],
            first_name=profile["user"]["first_name"],
            last_name=profile["user"]["last_name"],
        )
       
        Profile.objects.create(user=user,telephone=profile["telephone"])

def createUser(user):
    user = User.objects.create(
        username=user["username"],
        password=user["password"],
        first_name=user["first_name"],
        last_name=user["last_name"],
    )
    return user

###################################
kiosks = [
      {
        "nom": "LE PARISIEN",
        "addresse": "kinama",
        "NIF": "56264gvn",
        "RC": "8978",
        "contact": "79533729"
    },
    {
        "id": 2,
        "nom": "KATIKATI",
        "addresse": "Avenue de l'independance",
        "NIF": '',
        "RC": '',
        "contact": "simba234@gmail.com"
    }

]

def prepopulateKiosks():
    for kiosk in kiosks:
        kiosk = Kiosk.objects.create(
            nom=kiosk['nom'],
            addresse=kiosk['addresse'],
            NIF=kiosk['NIF'],
            RC=kiosk['RC'],
            contact=kiosk['contact']
        )
        kiosk.save()

def createKiosk(kiosk):
    kiosk = Kiosk.objects.create(
        nom = kiosk['nom'],
        addresse = kiosk['addresse'],
        NIF = kiosk['NIF'],
        RC =  kiosk['RC'],
        contact = kiosk['contact']
    )
    return kiosk
#################################
produits = [
    {
    "id":1,
    "nom": "ibitoke",
    "prix": 100,
    "quantite": 10,
    "kiosk": 1,
    },
    {
        "id":2,
        "nom": "ibiraya",
        "prix": 400,
        "quantite": 15,
        "kiosk": 2,
    }
]

def prepopulateProduits():
   for produit in produits:
        produit = Produit.objects.create(
            nom=produit['nom'],
            prix=produit['prix'],
            quantite=produit['quantite'],
            kiosk_id=produit['kiosk']  
        )
        produit.save()
def createproduit(produit):
     produit_cree = Produit.objects.create(
           nom = produit['nom'],
           prix = produit['prix'],
           quantite = produit['quantite'],
           kiosk = produit['kiosk']
       )
     return produit_cree

clients = [
    {
            "nom": "Eddy",
            # "addresse": "Kanyosha",
            "telephone": "+25760000453",
            "nif": "0023499",
            # "RC": "0098099",
    },
    {
            "nom": "Alida",
            # "addresse": "Gihosha",
            "telephone": "+25763000000",
            "nif": "002367",
            # "RC": "0098543",
    }
]

def prepopulateClients():
   for client in clients:
        client = Client.objects.create(
            nom=client['nom'],
            # addresse=client['addresse'],
            telephone=client['telephone'],
            nif=client['nif']  
            # RC = client['RC']
        )
        client.save()
def createclient(client):
     client_cree = Client.objects.create(
           nom = client['nom'],
        #    addresse = client['addresse'],
           telephone = client['telephone'],
           nif = client['nif']
        #    RC = client['RC']
       )
     return client_cree












# from api.models import Profile
# from django.contrib.auth.models import User

# profiles = [
#     {
#         "telephone":""
#         "username":{
#             "username":"NG",
#             "password":"dede1990"
#             "first_name":"",
#             "last_name":"",
#         }
#     }
# ],


# def prepopulateProfiles(profiles):
#     for profile in profiles:
#         user = User.objects.create(
#             username=profile["user"]["username"],
#             password=profile["user"]["password"],
#             first_name=profile["user"]["first_name"],
#             last_name=profile["user"]["last_name"],
#         )
       
#         Profile.objects.create(user=user,telephone=profile["telephone"])

# def createUser(user):
#     user = User.objects.create(
#         username=user["username"],
#         password=user["password"],
#         first_name=user["first_name"],
#         last_name=user["last_name"],
#     )
#     return user