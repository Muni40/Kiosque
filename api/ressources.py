from import_export import resources
from .models import *


class ProduitResource(resources.ModelResource):
    class Meta:
        model = Produit