import os
_basedir = os.path.abspath(os.path.dirname(__file__))

DEBUG = True

SECRET_KEY = 'really_secret_garage_story_singlo!($@%&)*!#$%*'

SECURITY_PASSWORD_HASH = 'pbkdf2_sha512'
SECURITY_PASSWORD_SALT = 'SALT_OF_SALT'

SQLALCHEMY_DATABASE_URI = 'mysql://root:singlogolf@34@localhost/garagestory'

UPLOAD_FOLDER = os.path.join(os.getcwd(), 'api/video')
