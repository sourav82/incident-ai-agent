from openai import AzureOpenAI
from app.config import OPENAI_ENDPOINT, OPENAI_KEY
import logging

logging.info(f"Open AI endpoint: {OPENAI_ENDPOINT}")
logging.info(f"Open AI Key: {OPENAI_KEY}")

client = AzureOpenAI(
    api_key=OPENAI_KEY,
    azure_endpoint=OPENAI_ENDPOINT,
    api_version="2024-02-01"
)