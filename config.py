import os 

class Config:
    SQLALCHEMY_DATABASE_URI=os.getenv('SQLALCHEMY')
    SQLALCHEMY_TRACK_MODIFICATIONS=False
    SECRET_KEY=os.getenv('KEY')
    