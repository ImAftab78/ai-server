from flask import Flask, request, jsonify
import requests
import os
import json
import random

app = Flask(__name__)

# 🔐 API key (Render environment variable)
API_KEY = os.environ.get("API_KEY")

@app.route("/ask", methods=["POST"])
def ask():
    prompt = request.json.get("prompt", "")

    system_prompt = """
You are a Roblox builder AI.

You MUST ALWAYS return at least 5 objects.
NEVER return an empty list.

ONLY return valid JSON. NO extra text.

Allowed types: tree, rock

Example format:
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
                # 🔥 stable free model
                "model": "mistralai/mistral-7b-instruct",
                "messages": [
                    {"role": "user", "content": system_prompt + "\nUser request: " + prompt}
                ]
            }
        )

        data = response.json()
        print("RAW API RESPONSE:", data)

        reply = data["choices"][0]["message"]["content"]

        # 🧠 Try parsing AI JSON
        try:
            parsed = json.loads(reply)

            # 🔴 If AI still returns empty → force fallback
            if not parsed.get("objects"):
                raise ValueError("Empty objects")

        except:
            print("⚠️ Using fallback objects")

            # 🔥 fallback objects (guaranteed spawn)
            fallback = {
                "objects": []
            }

            for i in range(5):
                fallback["objects"].append({
                    "type": random.choice(["tree", "rock"]),
                    "position": [
                        random.randint(-20, 20),
                        0,
                        random.randint(-20, 20)
                    ]
                })

            reply = json.dumps(fallback)

        return jsonify({"reply": reply})

    except Exception as e:
        print("ERROR:", e)

        # 🔥 emergency fallback
        return jsonify({
            "reply": json.dumps({
                "objects": [
                    {"type": "tree", "position": [0, 0, 0]},
                    {"type": "rock", "position": [5, 0, 5]},
                    {"type": "tree", "position": [-5, 0, 3]}
                ]
            })
        })

if __name__ == "__main__":
    app.run(port=3000)
