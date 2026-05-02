from flask import Flask, request, jsonify
import requests
import os
import json
import random

app = Flask(__name__)

API_KEY = os.environ.get("API_KEY")

@app.route("/ask", methods=["POST"])
def ask():
    prompt = request.json.get("prompt", "")

    system_prompt = """
You are a Roblox AI builder.

Convert user input into actions.

You MUST always return valid JSON.
NEVER return empty actions.

Format:
{
 "actions":[
  {"type":"spawn","object":"tree","position":[0,0,0]},
  {"type":"spawn","object":"rock","position":[5,0,5]},
  {"type":"delete","object":"rock"},
  {"type":"modify","object":"tree","size":8}
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
                    {"role": "user", "content": system_prompt + "\nUser: " + prompt}
                ]
            }
        )

        data = response.json()
        reply = data["choices"][0]["message"]["content"]

        print("AI RAW:", reply)

        try:
            parsed = json.loads(reply)
            if not parsed.get("actions"):
                raise ValueError("Empty actions")
        except:
            print("⚠️ Using fallback")

            parsed = {
                "actions": []
            }

            for i in range(5):
                parsed["actions"].append({
                    "type": "spawn",
                    "object": random.choice(["tree", "rock"]),
                    "position": [random.randint(-20,20), 0, random.randint(-20,20)]
                })

            reply = json.dumps(parsed)

        return jsonify({"reply": reply})

    except Exception as e:
        print("ERROR:", e)

        return jsonify({
            "reply": json.dumps({
                "actions":[
                    {"type":"spawn","object":"tree","position":[0,0,0]}
                ]
            })
        })

if __name__ == "__main__":
    app.run(port=3000)
