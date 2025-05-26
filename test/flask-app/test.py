# To run this code you need to install the following dependencies:
# pip install google-genai

import base64
import os
from google import genai
from google.genai import types


def generate():
    client = genai.Client(
        api_key="AIzaSyCyWw7UXnyepu89ady39ZF0QBkV5Mo8N50"
    )

    model = "learnlm-2.0-flash-experimental"
    contents = [
        types.Content(
            role="user",
            parts=[
                types.Part.from_text(text="""Question: "You witness a group of teenagers vandalizing a holiday display in a mall. How do you react? "Options: A: 'Quietly observe and report to mall management without confronting them.', B: 'Intervene immediately, asking them to stop and leave the mall.', C: 'Take video or photos to use as evidence later.', D: 'Call the police and wait for them to arrive before taking any action.'"""),
            ],
        ),
    ]
    generate_content_config = types.GenerateContentConfig(
        response_mime_type="application/json",
        response_schema=genai.types.Schema(
            type = genai.types.Type.OBJECT,
            required = ["Correct Answer", "Option Analysis"],
            properties = {
                "Correct Answer": genai.types.Schema(
                    type = genai.types.Type.STRING,
                    description = "The letter corresponding to the most appropriate response.",
                    enum = ["A", "B", "C", "D"],
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
                    },
                ),
            },
        ),
    )

    for chunk in client.models.generate_content_stream(
        model=model,
        contents=contents,
        config=generate_content_config,
    ):
        print(chunk.text, end="")

if __name__ == "__main__":
    generate()
