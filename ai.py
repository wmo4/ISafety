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
        # Stream response from Ollama
        with requests.post(
            "http://localhost:11434/api/generate",
            json={"model": "phi3", "prompt": user_input},
            stream=True,
        ) as response:

            full_reply = ""
            for line in response.iter_lines():
                if not line:
                    continue
                decoded = line.decode("utf-8")
                if decoded.startswith("data: "):
                    data = decoded[6:]
                    if data.strip() == "[DONE]":
                        break
                    try:
                        obj = json.loads(data)
                        if "response" in obj:
                            full_reply += obj["response"]
                    except Exception:
                        continue

        # If Ollama didn’t return anything, say so
        if not full_reply.strip():
            full_reply = "⚠️ Ollama did not return a response."

        return jsonify({"response": full_reply.strip()})

    except Exception as e:
        return jsonify({"response": f"Error: {str(e)}"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
