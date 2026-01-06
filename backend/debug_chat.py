import requests
import json

url = "http://127.0.0.1:8000/api/chat"
payload = {
    "question": "What is the health score?",
    "context": {
        "scores": {"health_score": 85},
        "metadata": {"rows": 100}
    }
}

try:
    response = requests.post(url, json=payload)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.text}")
except Exception as e:
    print(f"Error: {e}")
