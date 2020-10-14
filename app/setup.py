
from dotenv import load_dotenv
import certifi
import os

# Set correct SSL certificate
os.environ['SSL_CERT_FILE'] = certifi.where()

# Initialize environment variables
ENVIRONMENT = os.getenv('ENVIRONMENT')
assert(ENVIRONMENT in [None, "testing"])

load_dotenv()

assert(all([
    isinstance(os.getenv(env_var), str) for env_var in [
        'ENVIRONMENT',
        'MONGO_DB_CONNECTION_STRING',
        'PASSWORD_SALT',
        'SECRET_KEY',
        'HASH_ALGORITHM',
        'ACCESS_TOKEN_EXPIRE_MINUTES',
        'MAILGUN_API_KEY',
        'ADMIN_FRONTEND_URL',
        'AUTH_BACKEND_URL'
    ]
]))
assert(os.getenv('ENVIRONMENT') in ['production', 'development', 'testing'])
assert(os.getenv('ACCESS_TOKEN_EXPIRE_MINUTES').isnumeric)

# Set environment if 'testing' has not already been set
ENVIRONMENT = os.getenv('ENVIRONMENT') if ENVIRONMENT is None else ENVIRONMENT

MONGO_DB_CONNECTION_STRING = os.getenv('MONGO_DB_CONNECTION_STRING')
PASSWORD_SALT = os.getenv('PASSWORD_SALT')
SECRET_KEY = os.getenv('SECRET_KEY')
HASH_ALGORITHM = os.getenv('HASH_ALGORITHM')
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv('ACCESS_TOKEN_EXPIRE_MINUTES'))
MAILGUN_API_KEY = os.getenv('MAILGUN_API_KEY')
ADMIN_FRONTEND_URL = os.getenv('ADMIN_FRONTEND_URL')
AUTH_BACKEND_URL = os.getenv('AUTH_BACKEND_URL')
