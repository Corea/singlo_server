import os
_basedir = os.path.abspath(os.path.dirname(__file__))

DEBUG = True

SECRET_KEY = 'really_secret_garage_story_singlo!($@%&)*!#$%*'

SECURITY_PASSWORD_HASH = 'pbkdf2_sha512'
SECURITY_PASSWORD_SALT = 'SALT_OF_SALT'

SQLALCHEMY_DATABASE_URI = 'mysql://root:singlogolf@34@localhost/garagestory'

UPLOAD_FOLDER = '/home/garagestory/singlo_server/api/video' #os.path.join(os.getcwd(), 'api/video')
CAPTURE_FOLDER = '/home/garagestory/singlo_server/api/capture' #os.path.join(os.getcwd(), 'api/capture')
PROFILE_FOLDER = '/home/garagestory/singlo_server/api/profile' #os.path.join(os.getcwd(), 'api/profile')

GCM_APIKEY = 'AIzaSyBDkxqu_qW1LofgPLhaSfUoRQIw16WOSY4'
