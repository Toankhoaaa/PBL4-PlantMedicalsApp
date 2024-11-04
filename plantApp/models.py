# app/models.py
from .extensions import db
class Plant(db.Model):
    __tablename__ = 'plants'
    plant_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    scientific_name = db.Column(db.String(100))
    description = db.Column(db.Text)
    image_url = db.Column(db.String(200))
    family = db.Column(db.String(100))

    # Relationships
    medicinal_uses = db.relationship('MedicinalUse', backref='plant', lazy=True)
    chemical_components = db.relationship('ChemicalComponent', backref='plant', lazy=True)
    regions = db.relationship('Region', secondary='plant_regions', backref='plants', lazy='dynamic')


class MedicinalUse(db.Model):
    __tablename__ = 'medicinal_uses'
    use_id = db.Column(db.Integer, primary_key=True)
    plant_id = db.Column(db.Integer, db.ForeignKey('plants.plant_id'), nullable=False)
    application = db.Column(db.String(200), nullable=False)
    preparation_method = db.Column(db.Text)
    dose = db.Column(db.String(50))


class ChemicalComponent(db.Model):
    __tablename__ = 'chemical_components'
    component_id = db.Column(db.Integer, primary_key=True)
    plant_id = db.Column(db.Integer, db.ForeignKey('plants.plant_id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    quantity = db.Column(db.String(50))


class Region(db.Model):
    __tablename__ = 'regions'
    region_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)


class PlantRegion(db.Model):
    __tablename__ = 'plant_regions'
    plant_id = db.Column(db.Integer, db.ForeignKey('plants.plant_id'), primary_key=True)
    region_id = db.Column(db.Integer, db.ForeignKey('regions.region_id'), primary_key=True)
