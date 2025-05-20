import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'your-secret-key-here'
    API_KEY = "1377836fd8c2ecb2382bb3dd08d1f071"
    API_URL = "https://papi.tanksblitz.ru/wotb"
    AUTH_URL = "https://api.tanki.su/wot/auth/login/"
    REDIRECT_URI = "http://localhost:5000/auth"  # Измените для продакшена
