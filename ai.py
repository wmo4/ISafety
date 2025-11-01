from flask import Flask, render_template_string, request, jsonify
import requests
import json

app = Flask(__name__, static_url_path='', static_folder='.')

# Keep chat history in memory (reset on restart)
chat_history = []

@app.route('/')
def home():
    with open("ai.html", "r", encoding="utf-8") as f:
        return render_template_string(f.read())

@app.route('/chat', methods=['POST'])
def chat():
    global chat_history
    user_input = request.json.get("prompt", "").strip()
    if not user_input:
        return jsonify({"response": "No input received."})

    # Append user message to chat history
    chat_history.append({"role": "user", "content": user_input})

    # Create a conversation-style prompt
    conversation = ""
    for msg in chat_history[-10:]:  # only last 10 exchanges for brevity
        role = "User" if msg["role"] == "user" else "AI"
        conversation += f"{role}: {msg['content']}\n"
    conversation += "AI:"

    try:
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={"model": "phi3", "prompt": conversation},
            stream=True,
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

        full_reply = full_reply.strip() or "⚠️ No text received from Ollama."
        chat_history.append({"role": "ai", "content": full_reply})
        return jsonify({"response": full_reply})

    except Exception as e:
        return jsonify({"response": f"Error: {str(e)}"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
