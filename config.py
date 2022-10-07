from os import getenv
from dotenv import load_dotenv

load_dotenv()

class Settings:
    db_url = getenv('DATABASE_URL')
    host = getenv('HOST')
    port = getenv('PORT')

settings = Settings()