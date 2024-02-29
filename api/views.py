from rest_framework import viewsets, mixins
from django.shortcuts import render
from .models import *
from .serializers import *
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt import authentication
from rest_framework.response import Response
from rest_framework.decorators import action

class ProfileViewset(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer

    http_method_names = ['get', 'post', 'put', 'patch', 'delete']
    permission_classes = [AllowAny]
    #authentication_classes = authentication.JWTAuthentication.SessionAuthentication
    # we can override crud
    # def create(self,request, *args, **kwargs):
    #     serializer = ProfileSerializer(data=request.data)
    #     validated_data=serializer.is_valid(raise_exception=True)
    #     print(validated_data)
    #     return Response({'status':"tuzoba turagira creation"})


    # queryset = User.objects.all()
    # serializer_class = UserSerializer

    @action(detail=False, methods=['post'],serializer_class=Change_PasswordSerializer)
    def reset_password(self, request):
        serializer = Change_PasswordSerializer(data = request.data)
        if serializer.is_valid():
            old_password = serializer.validated_data['old_password']
            new_password = serializer.validated_data['new_password']
            confirm_password = serializer.validated_data['confirm_password']
            user = request.user
            
            if (user.check_password(old_password) and new_password == confirm_password):
                user.set_password(new_password)
                user.save()
                
            else:
                return Response({'status': 'Passwords do not match'}, status=400)
            
            return Response({'status':"password changed"},200)
    
        return Response(serializer.errors, 400),

        # print(request)
        # print(dir(request))
        # print(request.data)
        #request= request.data
                #ubundi buryo bwo kubikora ariko ifise ama failles
                # old_password = request.data.get('old_password')
                # new_password = request.data.get('new_password')
                # confirm_password = request.data.get('confirm_password')
                # user = request.user
        # 1ere methode
        # temp_user =User()
        # temp_user.set_password(old_password)
        # print("old",temp_user.password)
        # user=request.user
        # print("db password",user.password)
        # 2 eme methode
        # user=request.user
        # v=user.check_password(old_password)
        # print(v)

                #suite y'ubundi buryo bwo kubikora ariko ifise ama failles
                # if (user.check_password(old_password) and new_password == confirm_password):
                #     user.set_password(new_password)
                #     user.save()
                    
                # else:
                #     return Response({'status': 'Passwords do not match'}, status=400)
                
                # return Response({'status':"password changed"},200)
    


class AttributionsViewset(viewsets.ModelViewSet):
    queryset = Attribution.objects.all()
    serializer_class = AttributionsSerializer

class ProduitViewset(viewsets.ModelViewSet):
    queryset = Produit.objects.all()
    serializer_class = ProduitSerializer
    @action(detail=True, methods=['put'],serializer_class=Change_PrixSerializer)
    def modifier_addresse(self, request , pk=None):
     serializer = Change_PrixSerializer(data = request.data)
     if serializer.is_valid():
        produit = self.get_object()
        old_prix =serializer.validated_data['old_prix']
        new_prix = serializer.validated_data['new_prix']  
        confirm_prix = serializer.validated_data['confirm_prix']
       
        if (old_prix == old_prix and new_prix == confirm_prix):
             produit.prix = new_prix
             produit.save()
        else:
               return Response({'status': 'Prix do not match'}, status=400)
        
        return Response({'status':"Prix changed"},200)
     return Response(serializer.errors, 400)


class CommandeViewset(viewsets.ModelViewSet):
    queryset = Commande.objects.all()
    serializer_class = CommandeSerializer

    # def create(self, request,*args, **kwargs):
    #     serializer = CommandeSerializer(data=request.data)
    #     serializer.is_valid(raise_exception=True)
    #     vendeur = request.user.profile
    #     commande = Commande(vendeur=vendeur, **serializer.data)
    #     commande.save()
    #     serializer = CommandeSerializer(commande)
    #     return Response(serializer.data, status=201)

           # ou
    def perform_create(self, serializer):
        serializer.save(vendeur=self.request.user.profile)
        return serializer
    

class KioskViewset(viewsets.ModelViewSet):
    queryset = Kiosk.objects.all()
    serializer_class = KioskSerializer
    permission_classes = [AllowAny]
    actions = ["modifier_addresse","new_kiosk"]

    @action(detail=True, methods=['put'],serializer_class=Change_AdresseSerializer)
    def modifier_addresse(self, request , pk=None):
     serializer = Change_AdresseSerializer(data = request.data)
     if serializer.is_valid():
        kiosk = self.get_object()
        old_addresse =serializer.validated_data['old_addresse']
        new_addresse = serializer.validated_data['new_addresse']  
        confirm_addresse = serializer.validated_data['confirm_addresse']
       
        if (old_addresse == old_addresse and new_addresse == confirm_addresse):
             kiosk.addresse = new_addresse
             kiosk.save()
        else:
               return Response({'status': 'Adrress do not match'}, status=400)
        
        return Response({'status':"Address changed"},200)
     return Response(serializer.errors, 400)
    
    @action(detail=False, methods=['post'],serializer_class=KioskSerializer)
    def new_kiosk(self, request):
        serializer = KioskSerializer(data = request.data)
        if serializer.is_valid():
            kiosks = Kiosk.objects.all()
            nom = serializer.validated_data['nom']
            addresse = serializer.validated_data['addresse']
            NIF = serializer.validated_data['NIF']
            RC = serializer.validated_data['RC']
            contact = serializer.validated_data['contact']

            kiosk_existant = Kiosk.objects.filter(nom=nom, addresse=addresse, contact=contact,RC=RC,NIF=NIF).exists()
            if kiosk_existant :
                print("ce kiosk est deja disponible")
                return Response({'status': 'ce kiosk est deja disponible'}, status=400)
            else:
                kiosk = Kiosk.objects.create(nom=nom, addresse=addresse, NIF=NIF, RC=RC, contact=contact)
                kiosk.save()
                # print("ce kiosk peut etre ajouter")
            return Response({'status': 'Nouveau kiosk ajouter'}, status=200)
            

    
        return Response(serializer.errors, 400),
    

class VenteViewset(viewsets.ModelViewSet):
    queryset = Vente.objects.all()
    serializer_class = VenteSerializer

class StocksViewset(viewsets.ModelViewSet):
    queryset = Stock.objects.all()
    serializer_class = StocksSerializer

class PerteViewset(viewsets.ModelViewSet):
    queryset = Perte.objects.all()
    serializer_class = PerteSerializer

class PaymentViewset(viewsets.ModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer

class ClientViewset(viewsets.ModelViewSet):
    queryset = Client.objects.all()
    serializer_class = ClientsSerializer
    actions = 'delete_client'

    @action(detail=True, methods=['delete'],serializer_class=ClientsSerializer)
    def delete_client(self, request,pk=None):
        serializer = ClientsSerializer(data = request.data)
        client = self.get_object()
        if client is not None:
            client.delete()
            
        else:
            return Response({'status': 'client non trouve'}, status=400)
        return Response({'status': 'client supprimer'}, status=200),
    
