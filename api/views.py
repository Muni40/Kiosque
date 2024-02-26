from rest_framework import viewsets, mixins
from django.shortcuts import render
from .models import *
from .serializers import *
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt import authentication
from rest_framework.response import Response

class ProfileViewset(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [AllowAny]
    #authentication_classes = authentication.JWTAuthentication.SessionAuthentication
    # we can override crud
    # def create(self,request, *args, **kwargs):
    #     serializer = ProfileSerializer(data=request.data)
    #     validated_data=serializer.is_valid(raise_exception=True)
    #     print(validated_data)
    #     return Response({'status':"tuzoba turagira creation"})

class AttributionsViewset(viewsets.ModelViewSet):
    queryset = Attribution.objects.all()
    serializer_class = AttributionsSerializer

class ProduitViewset(viewsets.ModelViewSet):
    queryset = Produit.objects.all()
    serializer_class = ProduitSerializer

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
