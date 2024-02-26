from .models import *
from rest_framework import serializers

class ProduitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Produit
        fields = "__all__"

class KioskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Kiosk
        fields = "__all__"

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = "__all__"

class AttributionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attribution
        fields = "__all__"

class CommandeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Commande
        fields = "__all__"
        exclude_fields = "vendeur"

class VenteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vente
        fields = "__all__"

class PaymentSerializer(serializers.ModelSerializer):
     class Meta:
         model = Payment
         fields = "__all__"       

class KioskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Kiosk
        fields = "__all__"

class StocksSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stock
        fields = "__all__"

class PerteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Perte
        fields = "__all__"

class ClientsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = "__all__"
