import os
from datetime import timedelta

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'mysecretkey')
    # Updated with new Neon database credentials
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        'DATABASE_URL',
        'postgresql://hrmsDB_owner:0zCK1tayDBVO@ep-nameless-tree-a5w3yb7w.us-east-2.aws.neon.tech/hrmsDB?sslmode=require'
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = 'your_jwt_secret_key'
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(days=1)
