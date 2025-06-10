import os
from dotenv import load_dotenv            
from ibm_watson import NaturalLanguageUnderstandingV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator

load_dotenv()

IBM_API_KEY = os.getenv("IBM_API_KEY")
IBM_API_URL = os.getenv("IBM_API_URL")

if not IBM_API_KEY or not IBM_API_URL:
    raise RuntimeError("Missing IBM_API_KEY or IBM_API_URL environment variables")

authenticator = IAMAuthenticator(IBM_API_KEY)
nlu = NaturalLanguageUnderstandingV1(
    version="2025-06-08",
    authenticator=authenticator
)
nlu.set_service_url(IBM_API_URL)