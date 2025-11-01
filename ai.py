from flask import Flask, render_template_string, request, jsonify
import requests
import json

app = Flask(__name__, static_url_path='', static_folder='.')

@app.route('/')
def home():
    with open("ai.html", "r", encoding="utf-8") as f:
        return render_template_string(f.read())

@app.route('/chat', methods=['POST'])
def chat():
    user_input = request.json.get("prompt")
    if not user_input:
        return jsonify({"response": "No input received."})

    try:
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={"model": "phi3", "prompt": user_input},
            stream=True
        )

        full_reply = ""
        for line in response.iter_lines():
            if not line:
                continue
            try:
                data = json.loads(line.decode("utf-8"))
                if "response" in data:
                    full_reply += data["response"]
                if data.get("done"):
                    break
            except json.JSONDecodeError:
                continue

        if not full_reply.strip():
            full_reply = "⚠️ No text received from Ollama."

        return jsonify({"response": full_reply.strip()})

    except Exception as e:
        return jsonify({"response": f"Error: {str(e)}"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
