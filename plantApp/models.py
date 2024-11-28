from flask_sqlalchemy import SQLAlchemy

# Khởi tạo SQLAlchemy
db = SQLAlchemy()

# Model Plants (Cây thuốc)
class Plant(db.Model):
    __tablename__ = 'plants'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    scientific_name = db.Column(db.String(255))
    family = db.Column(db.String(255))
    description = db.Column(db.Text)
    uses = db.Column(db.Text)
    image_url = db.Column(db.String(255))
    images = db.relationship('PlantImage', backref='plant', lazy=True)
    ingredients = db.relationship('Ingredient', backref='plant', lazy=True)
    regions = db.relationship('PlantRegion', backref='plant', lazy=True)

# Model Regions (Vùng phân bố)
class Region(db.Model):
    __tablename__ = 'regions'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    plants = db.relationship('PlantRegion', backref='region', lazy=True)

# Model Plant_Regions (Liên kết cây thuốc với vùng phân bố)
class PlantImage(db.Model):
    __tablename__ = 'plant_images'
    id = db.Column(db.Integer, primary_key=True)
    plant_id = db.Column(db.Integer, db.ForeignKey('plants.id', ondelete='CASCADE'), nullable=False)  # Thêm ON DELETE CASCADE
    image = db.Column(db.String(255))

class Ingredient(db.Model):
    __tablename__ = 'ingredients'
    id = db.Column(db.Integer, primary_key=True)
    plant_id = db.Column(
        db.Integer,
        db.ForeignKey('plants.id', ondelete='CASCADE', name='fk_ingredient_plant'),
        nullable=False
    )
    name = db.Column(db.String(255), nullable=False)
    effect = db.Column(db.Text, nullable=False)

class PlantRegion(db.Model):
    __tablename__ = 'plant_regions'
    id = db.Column(db.Integer, primary_key=True)
    plant_id = db.Column(db.Integer, db.ForeignKey('plants.id', ondelete='CASCADE'), nullable=False)  # Thêm ON DELETE CASCADE
    region_id = db.Column(db.Integer, db.ForeignKey('regions.id'), nullable=False)

class Documentation(db.Model):
    __tablename__ = 'documentation'
    id = db.Column(db.Integer, primary_key=True)
    plant_id = db.Column(db.Integer, db.ForeignKey('plants.id', ondelete='CASCADE'), nullable=False)
    title = db.Column(db.String(255), nullable=False, default='Documentation', server_default='Documentation')
    url = db.Column(db.String(255), nullable=False)


