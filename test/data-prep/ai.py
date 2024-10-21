import google.generativeai as genai
from dotenv import load_dotenv
import os

load_dotenv()

genai.configure(api_key=os.environ["API_KEY"])


model = genai.GenerativeModel("gemini-1.5-flash")
response = model.generate_content("Question: A resident asks you to give them access to their unit, as they lost their key. The management only uses Master Key for emergencies. What will be your response? Options: A. Ignore the resident. B. Give them access C. Ask the resident to get a locksmith, as management doesn't allow access D. Give them the master key. ")
print(response.text)


