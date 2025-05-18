import os
from dotenv import load_dotenv

load_dotenv()

# app/config.py
class Config:
    MONGO_URI = "mongodb://localhost:27017/my_mvp_app"
    JWT_SECRET_KEY = "6HPFW3INuRkpko4jGQkp9K98ecvokCZuBRlNi5kxfOI"
