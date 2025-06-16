# app.py
import os
import json
from flask import Flask, request, render_template, jsonify
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables from .env file if it exists (for local development)
load_dotenv()

# Get API key from environment variable
api_key = os.getenv('OPENAI_API_KEY')
if not api_key:
    raise RuntimeError("OPENAI_API_KEY environment variable is not set")

# Instantiate the OpenAI client with explicit API key
client = OpenAI(api_key=api_key)

# 3) Read the instructions + schema from prompt.txt at startup
PROMPT_FILE = os.path.join(os.path.dirname(__file__), "prompt.txt")
try:
    with open(PROMPT_FILE, "r", encoding="utf-8") as f:
        instructions = f.read()
except FileNotFoundError:
    raise RuntimeError(f"Could not find {PROMPT_FILE}. Make sure it exists next to app.py")

# 4) Define your three pre-written "user queries" (replace these with whatever you want)
PRE_WRITTEN_INPUTS = {
    "prompt1": "Create a security/concierge protocol behavioral mcq at a Commercial location.",
    "prompt2": "Create a security/concierge protocol behavioral mcq at a Residential location.",
    "prompt3": "Create a security/concierge protocol behavioral mcq at an Event location."
}

# 5) Your fine-tuned GPT-4o-mini model name/ID
FINE_TUNED_MODEL = "gpt-4o-mini"

app = Flask(__name__, template_folder="templates")


@app.route("/prompt-test")
def index():
    """
    Render the HTML page with three buttons and an empty response box.
    """
    return render_template("prompt-test.html")


@app.route("/generate", methods=["POST"])
def generate():
    """
    Expects a JSON payload: { "prompt_id": "prompt1" }
    Combines `instructions` (as a system message) + the user's query (as a user message),
    sends them to chat.completions.create, and returns the JSON-parsed output.
    """
    data = request.get_json(force=True)
    prompt_id = data.get("prompt_id", "")

    if prompt_id not in PRE_WRITTEN_INPUTS:
        return (
            jsonify({"error": "Invalid prompt_id. Use 'prompt1', 'prompt2', or 'prompt3'."}),
            400,
        )

    user_input = PRE_WRITTEN_INPUTS[prompt_id]

    try:
        # 6) Call the chat completion endpoint with instructions as "system"
        response = client.chat.completions.create(
            model=FINE_TUNED_MODEL,
            messages=[
                {"role": "system", "content": instructions},
                {"role": "user", "content": user_input}
            ],
            temperature=0.7,
            max_tokens=300
        )

        # 7) Extract the generated content
        generated_text = response.choices[0].message.content


        return jsonify({"response": generated_text})

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    # By default, Flask runs on http://127.0.0.1:5000
    app.run(debug=True)
