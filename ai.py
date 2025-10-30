from flask import Flask, render_template_string, request, jsonify
import requests

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
            stream=False
        )
        result = response.json()
        reply = result.get("response", "No reply generated.")
        return jsonify({"response": reply})
    except Exception as e:
        return jsonify({"response": f"Error: {str(e)}"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
