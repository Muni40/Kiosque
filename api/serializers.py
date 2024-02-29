from .models import *
from rest_framework import serializers

class ProduitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Produit
        fields = "__all__"
class Change_PrixSerializer(serializers.Serializer):
    old_prix= serializers.CharField()
    new_prix= serializers.CharField()
    confirm_prix= serializers.CharField(required=True)

class KioskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Kiosk
        fields = "__all__"

class Change_AdresseSerializer(serializers.Serializer):
    old_addresse= serializers.CharField()
    new_addresse= serializers.CharField()
    confirm_addresse= serializers.CharField(required=True)

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = "__all__"

class Change_PasswordSerializer(serializers.Serializer):
    old_password= serializers.CharField()
    new_password= serializers.CharField()
    confirm_password= serializers.CharField(required=True)

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


    