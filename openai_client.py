import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()  # 👈 Needed to load the key from .env

api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise ValueError("❌ OPENAI_API_KEY not found in environment!")

client = OpenAI(api_key=api_key)
client.api_type = "openai"
client.api_base = "https://api.openai.com/v1"   
