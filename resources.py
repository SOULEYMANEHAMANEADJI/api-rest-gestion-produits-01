from flask import request
from flask_restful import Resource
from marshmallow import ValidationError

from models import Product, db
from schemas import ProductSchema

# Définition de la ressource produit
class ProductResource(Resource):
    # Initialisation des schémas pour la validation et la sérialisation/désérialisation
    product_schema = ProductSchema()
    product_list_schema = ProductSchema(many=True)
    product_patch_schema = ProductSchema(partial=True)

    # Méthode GET pour récupérer un ou plusieurs produits
    def get(self, product_id=None):
        if product_id:
            # Si un id de produit est fourni, récupérer ce produit
            product = Product.query.get_or_404(product_id)
            return self.product_schema.dump(product)
        else:
            # Sinon, récupérer tous les produits
            all_products = Product.query.all()
            return self.product_list_schema.dump(all_products)

    # Méthode POST pour créer un nouveau produit
    def post(self):
        try:
            # Valider les données entrantes avec le schéma du produit
            new_product_data = self.product_schema.load(request.json)
        except ValidationError as err:
            # En cas d'erreur de validation, renvoyer un message d'erreur
            return {'message': 'Validation Error', 'errors': err.messages}, 400

        # Créer un nouveau produit avec les données validées
        new_product = Product(
            name=new_product_data['name'],
            description=new_product_data['description'],
            price=new_product_data['price'],
        )
        # Ajouter le nouveau produit à la session et valider les modifications
        db.session.add(new_product)
        db.session.commit()
        # Renvoyer le nouveau produit créé
        return self.product_schema.dump(new_product)

    # Méthode PUT pour mettre à jour un produit existant
    def put(self, product_id):
        try:
            # Valider les données entrantes avec le schéma du produit
            new_product_data = self.product_schema.load(request.json)
        except ValidationError as err:
            # En cas d'erreur de validation, renvoyer un message d'erreur
            return {'message': 'Validation Error', 'errors': err.messages}, 400

        # Récupérer le produit à mettre à jour
        product = Product.query.get_or_404(product_id)
        # Mettre à jour les attributs du produit avec les nouvelles données
        for key, value in new_product_data.items():
            if value is not None:
                setattr(product, key, value)
        # Valider les modifications
        db.session.commit()
        # Renvoyer le produit mis à jour
        return self.product_schema.dump(product)

    # Méthode PATCH pour mettre à jour partiellement un produit existant
    def patch(self, product_id):
        try:
            # Valider les données entrantes avec le schéma du produit (partiel)
            new_product_data = self.product_patch_schema.load(request.json)
        except ValidationError as err:
            # En cas d'erreur de validation, renvoyer un message d'erreur
            return {'message': 'Validation Error', 'errors': err.messages}, 400

        # Récupérer le produit à mettre à jour
        product = Product.query.get_or_404(product_id)
        # Mettre à jour les attributs du produit avec les nouvelles données
        for key, value in new_product_data.items():
            if value is not None:
                setattr(product, key, value)
        # Valider les modifications
        db.session.commit()
        # Renvoyer le produit mis à jour
        return self.product_schema.dump(product)

    # Méthode DELETE pour supprimer un produit existant
    def delete(self, product_id):
        # Récupérer le produit à supprimer
        product = Product.query.get_or_404(product_id)
        # Supprimer le produit de la session et valider les modifications
        db.session.delete(product)
        db.session.commit()
        # Renvoyer un code de statut 204 pour indiquer que la suppression a réussi
        return '', 204