from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

# 🔐 Secure way
API_KEY = os.environ.get("API_KEY")

@app.route("/ask", methods=["POST"])
def ask():
    prompt = request.json.get("prompt")

    system_prompt = """
You are a Roblox builder AI.
ONLY reply in JSON.
DO NOT WRITE ANY TEXT.

Format:
{
 "objects":[
  {"type":"tree","position":[0,0,0]},
  {"type":"rock","position":[5,0,5]}
 ]
}
"""

    try:
        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {API_KEY}",
                "Content-Type": "application/json"
            },
            json={
                "model": "mistralai/mistral-7b-instruct",
                "messages": [
                    {"role": "user", "content": system_prompt + prompt}
                ]
            }
        )

        data = response.json()
        reply = data["choices"][0]["message"]["content"]

        return jsonify({"reply": reply})

    except Exception as e:
        print(e)
        return jsonify({"reply": '{"objects":[]}'})

if __name__ == "__main__":
    app.run(port=3000)