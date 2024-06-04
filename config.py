# import os

# class Config:
#     SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
#     SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
#         'mysql+pymysql://root:Lovelena0220&@localhost/BeautyAppointmentSystem'
#     SQLALCHEMY_TRACK_MODIFICATIONS = False
    
import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'a_secret_key'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'mysql+pymysql://root:Lovelena0220&@localhost/BeautyAppointmentSystem'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    
