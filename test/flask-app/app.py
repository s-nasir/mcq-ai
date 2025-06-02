from flask import Flask, request, render_template, jsonify
import json
from google import genai
from google.genai import types
from dotenv import load_dotenv
import os

app = Flask(__name__)

# ---- env variables ----
load_dotenv()
MODEL_NAME = os.getenv("MODEL_NAME")
API_KEY    = os.getenv("API_KEY")


# ---- date variables ----

quiz_data = [
    {
        "question": "As a security officer at a condominium complex, you receive a call from someone claiming to be a resident who has forgotten their access card. They are currently at the side gate and request that you remotely unlock it so they can enter. Company policy requires visual identification before granting access to anyone. The caller sounds urgent and insists they have an important meeting to attend. What should you do?",
        "options": {
            "A": "Unlock the gate remotely to assist the resident and maintain good customer relations.",
            "B": "Refuse to unlock the gate and advise the caller to use their access card as per policy.",
            "C": "Ask the caller to come to the main entrance where you can verify their identity before granting access.",
            "D": "Ignore the call, assuming it's a potential security threat attempting to gain unauthorized entry."
        },
        "correct_answer": "C"
    },
    {
        "question": "While on duty at the condominium's front desk, you receive a call from a local police officer who states that they are conducting an investigation related to one of the residents. The officer requests confidential information about the resident's schedule and access card logs. Company policy strictly prohibits sharing resident information without proper authorization or a warrant. The officer insists that the matter is urgent and that not cooperating could hinder a critical investigation. What should you do?",
        "options": {
            "A": "Provide the requested information immediately to assist with the police investigation.",
            "B": "Politely decline as you are not authorised to share information.",
            "C": "Ask the officer to come in person and provide official identification before sharing any information.",
            "D": "Request a warrant or escalate to upper management."
        },
        "correct_answer": "D"
    },
    {
        "question": "You are a security officer at a busy retail mall. During your patrol, you notice a person behaving suspiciously near a high-end electronics store. They are loitering near the entrance, frequently checking their watch, and seem to be communicating with someone via a hands-free device. Company policy requires you to report any suspicious activity and avoid direct confrontation unless there's an immediate threat. Just then, you overhear them mentioning specific store layouts and security camera locations. What should you do?",
        "options": {
            "A": "Confront the person immediately and demand to know their intentions.",
            "B": "Continue to observe them discreetly while informing mall security management of the situation. ",
            "C": "Ignore the behavior since they haven't committed any crime and might just be waiting for someone. ",
            "D": "Approach them casually to offer assistance and gauge their reaction."
        },
        "correct_answer": "B"
    },
    {
        "question": "While monitoring surveillance footage at a large department store, you notice an employee frequently entering a restricted stockroom area without authorization. Company policy states that only inventory managers are allowed in that area due to high-value merchandise. The employee is well-liked and has been with the company for years. Confronting them could create workplace tension, but ignoring the behavior might enable theft. What should you do?",
        "options": {
            "A": "Report the incident to upper management.",
            "B": "Confront the employee directly to ask why they are accessing the restricted area.",
            "C": "Ignore the situation to maintain workplace harmony, assuming there's a valid reason.",
            "D": "Increase surveillance on the employee to gather more evidence before taking action."
        },
        "correct_answer": "A"
    },
    {
        "question": "Question: While monitoring security cameras at a commercial research facility, you observe an unfamiliar person tailgating behind an authorized employee to access a secure area. The authorized employee appears unaware of the person following them. Company policy requires that all visitors be registered and escorted. Approaching unauthorized individuals can be risky, but failing to act might compromise sensitive information. What should you do?",
        "options": {
            "A": "Approach the unauthorized individual and the employee to confirmm their access authorization.",
            "B": "Ignore the incident, assuming the person is a new employee who you haven't met yet.",
            "C": "Make a general announcement over the intercom reminding employees about tailgating policies. ",
            "D": "Review the footage later to determine if any security breach occurred before taking action."
        },
        "correct_answer": "A"
    }
]



# ---- routes ----

@app.route("/", methods=["GET"])
def home():
    return render_template("index.html")

@app.route("/mcq", methods=["GET"])
def mcq():
    return render_template("mcq.html", quiz_data=quiz_data)

#   ---- MCQ PAGE Functions ----

@app.route("/get-ai-response", methods=["POST"])
def get_ai_response():
    data = request.json
    question = data.get("question")
    options = data.get("options")

    prompt_text = f'Question: "{question}"\nOptions:\n'
    prompt_text += "\n".join([f'{key}: "{value}"' for key, value in options.items()])

    client = genai.Client(api_key="AIzaSyCyWw7UXnyepu89ady39ZF0QBkV5Mo8N50")
    model = "learnlm-2.0-flash-experimental"  

    contents = [
        {
            "role": "user",
            "parts": [{"text": prompt_text}]
        }
    ]

    generate_content_config = types.GenerateContentConfig(
        response_mime_type="application/json",
        response_schema=genai.types.Schema(
            type=genai.types.Type.OBJECT,
            required=["Correct Answer", "Option Analysis"],
            properties={
                "Correct Answer": genai.types.Schema(
                    type=genai.types.Type.STRING,
                    enum=["A", "B", "C", "D"]
                ),
                "Option Analysis": genai.types.Schema(
                    type = genai.types.Type.OBJECT,
                    description = "Concise explanations for each option.",
                    required = ["A", "B", "C", "D"],
                    properties = {
                        "A": genai.types.Schema(
                            type = genai.types.Type.STRING,
                            description = "Brief analysis of why option A is appropriate or inappropriate (max 90 characters).",
                        ),
                        "B": genai.types.Schema(
                            type = genai.types.Type.STRING,
                            description = "Brief analysis of why option B is appropriate or inappropriate (max 90 characters).",
                        ),
                        "C": genai.types.Schema(
                            type = genai.types.Type.STRING,
                            description = "Brief analysis of why option C is appropriate or inappropriate (max 90 characters).",
                        ),
                        "D": genai.types.Schema(
                            type = genai.types.Type.STRING,
                            description = "Brief analysis of why option D is appropriate or inappropriate (max 90 characters).",
                        ),
                    }
                )
            }
        )
    )

    try:
        response = client.models.generate_content(
            model=model,
            contents=contents,
            config=generate_content_config
        )

    
        raw_json = response.candidates[0].content.parts[0].text
        structured_output = json.loads(raw_json)

        return jsonify(structured_output)

    except (IndexError, json.JSONDecodeError, Exception) as e:
        print(f"AI error: {e}")
        return jsonify({"error": "Failed to process AI response."})


#   ---- PROPMP PAGE Functions ----

@app.route("/prompt-box", methods=["GET", "POST"])
def prompt_box():
    prompt_text   = None
    structured   = None

    if request.method == "POST":
        prompt_text = request.form["prompt"]
        structured  = send_prompt_to_api(prompt_text)

    return render_template(
        "prompt-box.html",
        prompt=prompt_text,
        result=structured
    )

def send_prompt_to_api(prompt: str) -> dict:
    client = genai.Client(api_key=API_KEY)
    # build the same “Question… Options…” content block
    contents = [
        types.Content(
            role="user",
            parts=[ types.Part.from_text(text=prompt) ]
        )
    ]

    # exactly the same schema you used in test.py
    config = types.GenerateContentConfig(
        response_mime_type="application/json",
        response_schema=genai.types.Schema(
            type=genai.types.Type.OBJECT,
            required=["Correct Answer", "Option Analysis"],
            properties={
                "Correct Answer": genai.types.Schema(
                    type=genai.types.Type.STRING,
                    enum=["A", "B", "C", "D"]
                ),
                "Option Analysis": genai.types.Schema(
                    type=genai.types.Type.OBJECT,
                    required=["A", "B", "C", "D"],
                    properties={
                        "A": genai.types.Schema(type=genai.types.Type.STRING),
                        "B": genai.types.Schema(type=genai.types.Type.STRING),
                        "C": genai.types.Schema(type=genai.types.Type.STRING),
                        "D": genai.types.Schema(type=genai.types.Type.STRING),
                    }
                ),
            }
        )
    )

    try:
        resp = client.models.generate_content(
            model=MODEL_NAME,
            contents=contents,
            config=config
        )
        raw_json = resp.candidates[0].content.parts[0].text
        return json.loads(raw_json)

    except Exception as e:
        app.logger.error(f"Prompt-box AI error: {e}")
        return {"error": "Failed to parse AI response"}




if __name__ == "__main__":
    app.run(debug=True)