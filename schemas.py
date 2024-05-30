from flask_marshmallow import Marshmallow
from models import Product

# Initialiser Marshmallow
ma = Marshmallow()

# Définir le schéma du produit
class ProductSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        # Spécifier le modèle de produit à utiliser
        model = Product()