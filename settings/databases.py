import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

DATABASES = {
    'default': {
        'ENGINE': os.getenv('ENGINE'),
        'CLOUDFLARE_DATABASE_ID': os.getenv('CLOUDFLARE_DATABASE_ID'),
        'CLOUDFLARE_ACCOUNT_ID': os.getenv('CLOUDFLARE_ACCOUNT_ID'),
        'CLOUDFLARE_TOKEN': os.getenv('CLOUDFLARE_TOKEN'),
    }
}