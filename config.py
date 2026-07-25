import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY')
    if not SECRET_KEY:
        raise ValueError("SECRET_KEY environment variable is not set. Please set it in the .env file.")
    # Read SUPABASE_DB_URL from .env file
    raw_db_url = os.environ.get('SUPABASE_DB_URL')
    if raw_db_url and raw_db_url.startswith('postgresql://'):
        raw_db_url = raw_db_url.replace('postgresql://', 'postgresql+psycopg://', 1)
        
    SQLALCHEMY_DATABASE_URI = raw_db_url
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    if not SQLALCHEMY_DATABASE_URI:
        raise ValueError("SUPABASE_DB_URL environment variable is not set. Please set it in the .env file.")
