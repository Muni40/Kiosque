from rest_framework.test import APITestCase,APIClient
from .datas import prepopulateProfiles,prepopulateKiosks,User,prepopulateProduits,prepopulateClients
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer,RefreshToken
#from django.contrib.auth.models import User

class TestSetUp(APITestCase):
     def setUp(self)->None:
      user = {
         "username": "Franck",
         "password": "dede1990"
      }
      new_user = User.objects.create(username=user["username"], password=user["password"])
      tokens:RefreshToken = TokenObtainPairSerializer.get_token(new_user)
      token = str(tokens.access_token)
      prepopulateProfiles()
      prepopulateKiosks()
      prepopulateProduits() 
      prepopulateClients()
      self.client = APIClient()
      self.client.credentials(HTTP_AUTHORIZATION="Bearer"+ token)
      print("Bearer" + token)
      return super().setUp()
    #   prepopulateKiosks()
    #  # prepopulateCommandes()
    #   self.client = APIClient()
    #   return super().setUp()
     
     def tearDown(self)->None:
        return super().tearDown()
     
     
     
# class Test
     

   