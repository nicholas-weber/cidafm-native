import requests

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "mistral"  # You can change this to any model you've pulled

def call_llm(payload_data):
    afms = payload_data.get("afms", [])
    context = payload_data.get("context", [])
    user_input = payload_data.get("user_input", "")

    if user_input is None:
        return "[cidafm] No user input to process."

    afm_block = ", ".join(f"&{afm}" for afm in afms)
    context_block = "\n".join(context)

    prompt = f"""[AFMs]
{afm_block}

[Context]
{context_block}

[User]
{user_input}
"""

    print("[debug] Sending prompt to LLM...")
    print(prompt)

    payload = {
        "model": MODEL_NAME,
        "prompt": prompt,
        "stream": False
    }

    try:
        response = requests.post(OLLAMA_URL, json=payload)
        print("[debug] LLM response status:", response.status_code)
        response.raise_for_status()
        data = response.json()
        print("[debug] LLM raw response:", data)
        return data.get("response", "[cidafm] No response received.")
    except Exception as e:
        return f"[cidafm] LLM call failed: {e}"