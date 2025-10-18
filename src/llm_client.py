import requests
from .config import API_KEY, MODEL

def ask_llm(prompt: str) -> str:
    response = requests.post(
        "https://openrouter.ai/api/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {API_KEY}",
            "Content-Type": "application/json",
        },
        json={
            "model": MODEL,
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0.3,
        },
    )
    response.raise_for_status()
    data = response.json()
    return data["choices"][0]["message"]["content"].strip()
