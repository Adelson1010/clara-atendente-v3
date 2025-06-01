from flask import Flask, request, jsonify
from flask_cors import CORS
import openai
import os

app = Flask(__name__)
CORS(app)

openai.api_key = os.environ.get("OPENAI_API_KEY")

@app.route("/", methods=["GET"])
def index():
    return "Clara está ativa! 👋"

@app.route("/", methods=["POST"])
def responder():
    data = request.get_json()
    
    try:
        mensagem = data["message"]["text"]
        resposta = gerar_resposta(mensagem)
        return jsonify({"resposta": resposta})
    except Exception as e:
        return jsonify({"erro": str(e)}), 400

def gerar_resposta(mensagem):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "Você é uma atendente virtual chamada Clara, educada, acolhedora e inteligente. Seja breve, simpática e clara."},
            {"role": "user", "content": mensagem}
        ]
    )
    return response.choices[0].message["content"]

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
