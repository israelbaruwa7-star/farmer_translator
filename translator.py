import os
from dotenv import load_dotenv
import google.generativeai as genai

# Load environment variables
load_dotenv()

# Configure Gemini
api_key = os.getenv("GOOGLE_API_KEY")
if api_key:
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel("gemini-1.5-flash")
else:
    model = None  # fallback if no API key

def translate(text, target_language="English"):
    if not model:
        return f"MOCK: {text} -> ({target_language})"

    prompt = f"""
    Detect the language of the following text and translate it into {target_language}.
    If the text is already in {target_language}, just return it as-is.
    Text: {text}
    """
    response = model.generate_content(prompt)
    return response.text
