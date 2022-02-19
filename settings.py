import os
from dotenv import load_dotenv


API_TIMEOUT = 3600
GCORE_AUTH_URL = 'https://api.gcdn.co/auth/jwt/login'
BASE_URL = 'https://api.cloud.gcorelabs.com/v1'

load_dotenv()

USERNAME = str(os.getenv('GCORE_USERNAME'))
PASSWORD = str(os.getenv('GCORE_PASSWORD'))
