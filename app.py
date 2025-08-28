from flask import Flask, render_template, request
from translator import translate
from markupsafe import Markup

app = Flask(__name__)

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
