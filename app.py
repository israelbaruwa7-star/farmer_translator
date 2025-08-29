from flask import Flask, render_template, request
from markupsafe import Markup
import os
from dotenv import load_dotenv
import google.generativeai as genai

# Load environment variables (for local dev; on Render, set them in Dashboard)
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
    """Translate text into the target language using Gemini API (or mock)."""
    if not model:
        return f"MOCK: {text} -> ({target_language})"

    prompt = f"""
    Detect the language of the following text and translate it into {target_language}.
    If the text is already in {target_language}, just return it as-is.
    Text: {text}
    """
    response = model.generate_content(prompt)
    return response.text

# List of popular languages
LANGUAGES = [
    "English", "Yoruba", "Hausa", "Igbo", "French", "Spanish", "Portuguese",
    "Swahili", "Arabic", "German", "Chinese", "Japanese", "Korean", "Russian",
    "Hindi", "Bengali", "Turkish", "Italian", "Dutch", "Zulu"
]

def format_response(response_text):
    """Format Gemini output into HTML if it contains bullet/star lists."""
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
        result = format_response(raw_result)

    return render_template("index.html", result=result, languages=LANGUAGES)

if __name__ == "__main__":
    # ✅ Important for Render: bind to 0.0.0.0 and use provided PORT
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)
