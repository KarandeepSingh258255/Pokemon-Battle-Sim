from dotenv import load_dotenv
import os
from google import genai

load_dotenv()


client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])

def ask_gemini(prompt):
    response = client.generate_content()