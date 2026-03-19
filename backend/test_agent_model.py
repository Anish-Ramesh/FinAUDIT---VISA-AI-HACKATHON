from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
import os

load_dotenv()

key = os.environ.get("GOOGLE_API_KEY")
print(f"Testing with key starting with: {key[:5]}...")

try:
    llm = ChatGoogleGenerativeAI(
        model="gemini-3.1-pro-preview", 
        google_api_key=key
    )
    print(" invoking model...")
    res = llm.invoke("Hello, are you working?")
    print(f"Type of res: {type(res)}")
    print(f"Type of res.content: {type(res.content)}")
    print(f"Content: {res.content}")
except Exception as e:
    print(f"Error: {e}")
