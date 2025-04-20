from google import genai
import dotenv
dotenv.load_dotenv()
import os
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))



response = client.models.generate_content(
    model="gemini-2.0-flash",
 
    contents="Hello there"
)

print(response.text)

