from rest_framework.test import APITestCase,APIClient
from .test_setup import TestSetUp
from .datas import Kiosk,createKiosk,Profile,createUser,Produit,Client
from django.urls import reverse

class TestProfileViewSet(TestSetUp):
    profile_list_url = reverse('profile-list')
    def test_get_all_profiles(self):
        detail = "Get all Profiles"
        print(f"{detail:#^30}")
        res = self.client.get(self.profile_list_url)
        print(res.data)
        self.assertEqual(res.status_code, 200)

    # def test_get_profile_details(self):
    #     detail = "Get Profile Details"
    #     print(f"{detail:#^30}")
    #     url = reverse('profile-detail', kwargs={'pk':1})
    #     res = self.client.get(url)
    #     print(res.data)
    #     self.assertEqual(res.status_code, 200)

    def test_post_profile(self):
        detail = "Post Profile"
        print(f"{detail:=^30}")
        user = {
            "username":"celine",
            "password":"dede1990",
            "first_name":"celine",
            "last_name":"Irakoze",
    }
        created_user = createUser(user)
        data = {
            "telephone":"257 64321980",
            "user": created_user.id
        }
        res = self.client.post(self.profile_list_url,data)
        print(res.data)
        self.assertEqual(res.status_code, 201)

    
    def test_invalid_post_profile(self):
        detail = "Post Profile"
        print(f"{detail:=^30}")
        user = {
            "username":"celine",
            "password":"dede1990",
            "first_name":"celine",
            "last_name":"Irakoze",
    }
        created_user = createUser(user)
        data = {
            "telephone":"257 64321980",
           
        }
        res = self.client.post(self.profile_list_url,data)
        print(res.data)
        self.assertEqual(res.status_code, 201)


class TestKioskViewSet(TestSetUp):
    kiosk_list_url = reverse('kiosk-list')
    def test_get_all_kiosks(self):
        detail = "Get all Kiosks"
        print(f'{detail:=^30}')
        # url = reverse('kiosk-list')
        # response = self.client.get(url, format='json')
        res = self.client.get(self.kiosk_list_url)
        print(res.data)
        self.assertEqual(res.status_code, 200)

    def test_get_detail_kiosks(self):
        detail = 'Get Kiosks Detail'
        print(f'{detail:=^30}')
        url = reverse('kiosk-detail', kwargs={'pk': 1})
        res = self.client.get(url)
        self.assertEqual(res.status_code, 200)
        print(res.data)

    def test_post_kiosk(self):
        detail = 'Post Kiosks'
        print(f'{detail:=^30}')
        url = reverse('kiosk-list')
        data = {
            "id":3,
            "nom": "Kiosk 4",
            "addresse": "123 Main St",
            "NIF": "5626774gvn",
            "RC": "8998078",
            "contact": "68381368"
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, 201)
        print(response.data)

    def test_update_kiosk(self):
        detail = 'Update Kiosks'
        print(f'{detail:=^30}')
        url = reverse('kiosk-detail', kwargs={'pk': 1})
        data = {
            "nom": "Kiosk 5",
            "addresse": "Kigobe",
            "NIF": "5626774gvn",
            "RC": "8998078",
            "contact": "68381368"
        }
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Kiosk.objects.get(id=1).addresse, 'Kigobe')
        print(response.data)

    def test_delete_kiosk(self):
        url = reverse('kiosk-detail', kwargs={'pk': 1})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 204)
        self.assertEqual(Kiosk.objects.count(), 1)
        print(response.data)

# class TestCommandeViewset(TestSetUp):
#     def test_get_all_commandes(self):
#         detail = "Get all Commandes"
#         url = reverse('commande-list')
#         response = self.client.get(url, format='json')
#         self.assertEqual(response.status_code, 200)
#         self.assertEqual(len(response.data), 1)
#         print(response.data)

class TestProduitViewSet(TestSetUp):
    def test_get_produits(self):
        url = reverse('produit-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        print(response.data)
    
    def test_post_produit(self):
        url = reverse('produit-list')
        datas = {
            "id":6,
            "nom": "arachide",
            "prix": 1000,
            "quantite": 0,
            "kiosk":2
        }
        resp = self.client.post(url, datas, format='json')
        self.assertEqual(resp.status_code, 201)
        print(resp.data)
    
    def test_update_produit(self):
        url = reverse('produit-detail', kwargs={'pk': 1})
        data = {
            "nom": "arachide",
            "prix": 500,
            "quantite": 0,
            "kiosk":1
        }
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Produit.objects.get(id=1).nom, 'arachide')
        print(response.data)
    
    def test_delete_produit(self):
        url = reverse('produit-detail', kwargs={'pk': 1})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 204)
        self.assertEqual(Produit.objects.count(), 3)
        print(response.data)
################################

class TestClientViewSet(TestSetUp):
    def test_get_clients(self):
        url = reverse('client-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        print(response.data)
    
    def test_post_client(self):
        url = reverse('client-list')
        datas = {
            "id":1,
            "nom": "Barnabas",
            # "addresse": "Gihosha",
            "telephone": "+257 67890453",
            "nif": "23456",
            "RC": "8998078",

        }
        resp = self.client.post(url, datas, format='json')
        self.assertEqual(resp.status_code, 201)
        print(resp.data)
    
    def test_update_client(self):
        url = reverse('client-detail', kwargs={'pk': 1})
        data = {
             "id":1,
            "nom": "Meddy",
            # "addresse": "Nyakabiga",
            "telephone": "+257 63800453",
            "nif": "0023456",
            "RC": "0098078",
        }
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Client.objects.get(id=1).nom, 'arachide')
        print(response.data)
    
    def test_delete_produit(self):
        url = reverse('client-detail', kwargs={'pk': 1})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 204)
        self.assertEqual(Client.objects.count(), 3)
        print(response.data)

    def test_action_telephone(self):
        self.client.credentials()
        url= reverse('client-change-telephone-client',kwargs={'pk': 1})

        data = {
            'old_telephone': '+25760000453',
            'new_telephone': '68765432', 
            'confirm_telephone': '68765432'
        }
        print(url)
        print("client",Client.objects.get(id=1).telephone)
        response = self.client.post(url, data)     
        print(response.data)
        self.assertEqual(response.status_code, 200)


    def test_invalid_action_telephone(self):
        url= reverse('client-change-telephone-client',kwargs={'pk': 1})
        data = {'old_telephone': '25760000453', 'new_telephone': '68765432'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(Client.objects.get(id=3).telephone, '+25760000453')
        self.assertEqual(response.status_code, 400)







#  def setUp(self):
#         self.client = Client.objects.create(name='John Doe', telephone='1234567890')

#     def test_change_telephone_client_success(self):
#         url = reverse('client-change-telephone-client', kwargs={'pk': self.client.pk})
#         data = {'old_telephone': '1234567890', 'new_telephone': '9876543210', 'confirm_telephone': '9876543210'}
#         client = APIClient()
#         response = client.put(url, data, format='json')
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertEqual(Client.objects.get(pk=self.client.pk).telephone, '9876543210')










 # view = TestClientViewSet(actions={'get': 'change_telephone_client'})
        # request = self.factory.get(url, {'id_user': 2})
        # response = view(request)


# def test_GetUserAgenda(self):
#     request_url = f'Agenda/get_user_agenda/'
#     view = AgendaViewSet.as_view(actions={'get': 'retrieve'})
#     request = self.factory.get(request_url, {'id_user': 15})
#     response = view(request)
#     self.assertEqual(response.status_code, 400)


# from rest_framework import APITestCase
# from .test_setup import TestSetup
# #from .datas import createUser,Profile
# from django.urls import reverse
# from .datas import Kiosk,createKiosk

# class TestProfileViewSet(TestSetup):
#     profile_list_url = reverse('profile_list')
#     def test_get_all_profiles(self):
#         detail = "Get all Profiles"
#         print(f"{detail:#^30}")
#         res = self.client.get(self.profile_list_url)
#         print(res.data)
#         self.assertEqual(res.status_code, 200)

#     def test_get_profile_details(self):
#         detail = "Get Profile Details"
#         print(f"{detail:#^30}")
#         url = reverse('profile-detail', kwargs={'pk'})
#         res = self.client.get(url)
#         print(res.data)
#         self.assertEqual(res.status_code, 200)

#     def test_post_profile(self):
#         user = {
#             "username":"NG32",
#             "password":"dede1990",
#             "first_name":"Bertilla",
#             "last_name":"Irakoze",
#     }
#         created_user = createUser(user)
#         data = {
#             "telephone":"257 64321980",
#             "user": created_user.id
#         }
#         res = self.client.post(self.profile_list_url)
#         print(res.data)
#         self.assertEqual(res.status_code, 200)

#     #def test

# class TestKioskViewSet(TestSetup):
#     def test_get_kiosks(self):
#         url = reverse('kiosks-list')
#         response = self.client.get(url,format='json')
#         self.assertEqual(response.status_code, 200)
#         self.assertEqual(len(response.data), 1)
#         print(response.data)
