from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

# 🔐 API key from environment (Render)
API_KEY = os.environ.get("API_KEY")

@app.route("/ask", methods=["POST"])
def ask():
    prompt = request.json.get("prompt")

    # 🔥 Strong system prompt
    system_prompt = """
You are a Roblox builder AI.

You MUST always return at least 5 objects.
DO NOT return empty objects list.

ONLY return valid JSON. NO extra text.

Format:
{
 "objects":[
  {"type":"tree","position":[0,0,0]},
  {"type":"tree","position":[5,0,5]},
  {"type":"rock","position":[-5,0,3]},
  {"type":"tree","position":[2,0,-4]},
  {"type":"rock","position":[7,0,1]}
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
                # 🔥 Better free model
                "model": "openchat/openchat-3.5",
                "messages": [
                    {"role": "user", "content": system_prompt + "\nUser request: " + prompt}
                ]
            }
        )

        data = response.json()

        # 🔍 Debug (optional)
        print("RAW API RESPONSE:", data)

        reply = data["choices"][0]["message"]["content"]

        return jsonify({"reply": reply})

    except Exception as e:
        print("ERROR:", e)
        return jsonify({
            "reply": '{"objects":[{"type":"tree","position":[0,0,0]}]}'
        })

if __name__ == "__main__":
    app.run(port=3000)
