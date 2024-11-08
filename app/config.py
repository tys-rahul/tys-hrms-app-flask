import os
from datetime import timedelta

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'mysecretkey')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL','postgresql://hrmsappdb_user:0t5tOVkp8mfl51967Ar8f18Jbd8ThG1c@dpg-csmugr5umphs73av58m0-a.oregon-postgres.render.com/hrmsappdb')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = 'your_jwt_secret_key'
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(days=1)  
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    # SQLALCHEMY_DATABASE_URI = 'sqlite:///mydatabase.db'
    # external => postgresql://hrmsappdb_user:0t5tOVkp8mfl51967Ar8f18Jbd8ThG1c@dpg-csmugr5umphs73av58m0-a.oregon-postgres.render.com/hrmsappdb
    # internal => postgresql://hrmsappdb_user:0t5tOVkp8mfl51967Ar8f18Jbd8ThG1c@dpg-csmugr5umphs73av58m0-a/hrmsappdb
