from dotenv import load_dotenv
import os

load_dotenv()

print("GEMINI_API_KEY loaded:", bool(os.getenv("GEMINI_API_KEY")))
