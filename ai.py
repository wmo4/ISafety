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
        # Ask Ollama for a streamed response
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={"model": "phi3", "prompt": user_input},
            stream=True
        )

        full_reply = ""
        for line in response.iter_lines():
            if not line:
                continue
            # Each line starts with "data: "
            if line.decode("utf-8").startswith("data: "):
                data = line.decode("utf-8")[6:]
                if data.strip() == "[DONE]":
                    break
                try:
                    json_data = json.loads(data)
                    full_reply += json_data.get("response", "")
                except json.JSONDecodeError:
                    continue

        return jsonify({"response": full_reply.strip() or "No response generated."})

    except Exception as e:
        return jsonify({"response": f"Error: {str(e)}"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
