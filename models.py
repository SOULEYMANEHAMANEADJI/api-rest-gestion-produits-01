from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, String, Float

# Définir la classe de base pour les modèles SQLAlchemy
Base = declarative_base()

# Initialiser SQLAlchemy avec la classe de base définie
db = SQLAlchemy(model_class=Base)


# Définir la classe du modèle de produit
class Product(Base):
    # Nom de la table dans la base de données
    __tablename__ = 'products'

    # Définir les colonnes de la table
    id = Column(Integer, primary_key=True)  # Identifiant unique pour chaque produit
    name = Column(String, unique=True, index=True, nullable=False)  # Nom du produit, doit être unique et non nul
    description = Column(String, index=True, nullable=False)  # Description du produit, ne peut pas être nulle
    price = Column(Float, nullable=False)  # Prix du produit, ne peut pas être nul
