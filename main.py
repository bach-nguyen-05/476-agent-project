import os, json, textwrap, re, time, ast, operator as op
from self_consistency import solve_with_self_consistency
import requests

API_KEY  = "cse476"
API_BASE = "http://10.4.58.53:41701/v1"
MODEL    = "bens_model"

def call_model_chat_completions(prompt: str,
                                system: str = "You are a helpful assistant. Reply with only the final answer—no explanation.",
                                model: str = MODEL,
                                temperature: float = 0.0,
                                timeout: int = 60) -> dict:
    url = f"{API_BASE}/chat/completions"
    headers = {"Authorization": f"Bearer {API_KEY}", "Content-Type":  "application/json"}
    payload = {
        "model": model,
        "messages": [{"role": "system", "content": system},
                     {"role": "user",   "content": prompt}],
        "temperature": temperature,
        "max_tokens": 256,
    }
    try:
        resp = requests.post(url, headers=headers, json=payload, timeout=timeout)
        if resp.status_code == 200:
            data = resp.json()
            text = data.get("choices", [{}])[0].get("message", {}).get("content", "")
            return {"ok": True, "text": text, "raw": data, "status": resp.status_code, "error": None, "headers": dict(resp.headers)}
        else:
            try: err_text = resp.json()
            except Exception: err_text = resp.text
            return {"ok": False, "text": None, "raw": None, "status": resp.status_code, "error": str(err_text), "headers": dict(resp.headers)}
    except requests.RequestException as e:
        return {"ok": False, "text": None, "raw": None, "status": -1, "error": str(e), "headers": {}}
    

# Testing
if __name__ == "__main__":
    import json
    with open("cse_476_final_project_test_data.json", "r") as f:
        test_questions = json.load(f)

    for question in test_questions[:5]:
        question = question["input"]
        print(f"Question: {question}")
        solve_with_self_consistency(question)
