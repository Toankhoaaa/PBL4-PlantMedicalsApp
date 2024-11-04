# app/config.py
import os
from dotenv import load_dotenv

load_dotenv()  # Load biến môi trường từ file .env

class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URI', 'sqlite:///medicinal_plants.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.getenv('SECRET_KEY', 'your_secret_key')
