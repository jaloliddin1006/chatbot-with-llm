# app/utils/config.py

import os
from dotenv import load_dotenv

OPENAI_API_KEY = "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"
PINECONE_API_KEY = "pcsk_LkhN8_KgLNaYu4sgc8SifKPoSrMEoxHgoJG6kMJgebgPYyC5KZY2tnoqsTuAyPEHToqDD"
PROJECT_ID = "23b1ac01-f61e-4e96-826f-bff92659b1e7"
PINECONE_REGION = 'us-east-1'
PINECONE_CLOUD = 'aws'



load_dotenv()

class Config:
    """
    Configuration class to hold settings.
    """
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY', OPENAI_API_KEY)
    PINECONE_API_KEY = os.getenv('PINECONE_API_KEY', PINECONE_API_KEY)
    PINECONE_ENVIRONMENT = os.getenv('PINECONE_ENVIRONMENT', "us-west1-gcp-free")
    # PROVIDER_ID = os.getenv('PROVIDER_ID')
    # AUTH_TOKEN = os.getenv('AUTH_TOKEN')
    # TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
    # WEBHOOK_URL = os.getenv('WEBHOOK_URL')
    # List of URLs to scrape
    URL_LIST = [
        "https://stat.uz/uz/haqida/rahbariyat",
        "https://stat.uz/uz/haqida/markaziy-apparat",
        ]

