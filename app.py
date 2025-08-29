from flask import Flask, render_template, request
from translator import translate
from markupsafe import Markup
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

app = Flask(__name__)

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

# List of popular languages (you can add/remove)
LANGUAGES = [
    "English", "Yoruba", "Hausa", "Igbo", "French", "Spanish", "Portuguese",
    "Swahili", "Arabic", "German", "Chinese", "Japanese", "Korean", "Russian",
    "Hindi", "Bengali", "Turkish", "Italian", "Dutch", "Zulu"
]

def format_response(response_text):
    # Split into lines where a star (*) starts an item
    lines = response_text.split("*")
    formatted_items = []

    for line in lines:
        line = line.strip()
        if line:
            formatted_items.append(f"<li>{line}</li>")

    if formatted_items:
        return Markup("<ol>" + "".join(formatted_items) + "</ol>")
    else:
        return response_text

@app.route("/", methods=["GET", "POST"])
def home():
    result = None
    if request.method == "POST":
        text = request.form["text"]
        target_language = request.form["target_language"]

        raw_result = translate(text, target_language)
        result = format_response(raw_result)   # ✅ Apply formatting here

    return render_template("index.html", result=result, languages=LANGUAGES)

if __name__ == "__main__":
    app.run(debug=True)


