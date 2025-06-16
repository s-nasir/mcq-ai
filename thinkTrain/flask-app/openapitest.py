from openai import OpenAI
client = OpenAI()

with open("prompt.txt", "r", encoding="utf-8") as f:
    instructions = f.read()

response = client.responses.create(
    model="gpt-4o-mini",
    instructions=instructions,
    input="Create a security/concierge protocol behavioral mcq at a commercial location.",
)

print(response.output_text)
