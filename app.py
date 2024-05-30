from flask import Flask
from flask_restful import Api

from models import db, Product
from resources import ProductResource
from schemas import ma

# Initialiser l'application Flask
app = Flask(__name__)
# Configurer la base de données
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///products.db'
# Initialiser SQLAlchemy et Marshmallow avec l'application
db.init_app(app)
ma.init_app(app)
# Initialiser l'API RESTful
api = Api(app)
# Ajouter la ressource produit à l'API
api.add_resource(ProductResource, '/products', '/products/<int:product_id>')

# Créer et configurer la base de données
with app.app_context():
    try:
        # Supprimer toutes les tables existantes
        db.drop_all()
        # Créer toutes les tables
        db.create_all()

        # Créer deux produits
        chaussure = Product(name='Chaussure', description='Une paire de chaussure', price='20.99')
        armoire = Product(name='Armoire', description='Une belle armoire', price='120.99')

        # Ajouter les produits à la session et valider les modifications
        db.session.add(chaussure)
        db.session.add(armoire)
        db.session.commit()
        print('DONE')

        # Récupérer les produits de la base de données
        chaussure_db = db.session.query(Product).filter(Product.name == 'Chaussure').first()
        armoire_db = db.session.query(Product).filter(Product.name == 'Armoire').first()

        # Afficher les informations des produits
        print(f"{chaussure_db.id} : {chaussure_db.name} - {chaussure_db.description}")
        print(f"{armoire_db.id} : {armoire_db.name} - {armoire_db.description}")

        # Démarrer l'application
        app.run(debug=True)
    except Exception as e:
        # En cas d'erreur, afficher le message d'erreur
        print(e)