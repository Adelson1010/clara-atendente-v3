from flask import Flask, request
import openai
import os
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

openai.api_key = os.getenv("OPENAI_API_KEY")

@app.route("/", methods=["POST"])
def responder():
    data = request.json

    # Verifica se é uma mensagem válida
    if data.get("type") == "message" and "text" in data.get("message", {}):
        telefone = data["phone"]
        mensagem = data["message"]["text"]

        resposta = gerar_resposta(mensagem)

        return {
            "send": [{
                "phone": telefone,
                "message": resposta
            }]
        }

    return "ok"

def gerar_resposta(mensagem):
    prompt = f"Você é uma atendente virtual chamada Clara. Seja educada e simpática. Responda a seguinte mensagem:\nUsuário: {mensagem}\nClara:"
    
    resposta = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7,
        max_tokens=100
    )

    return resposta.choices[0].message["content"].strip()

@app.route("/", methods=["GET"])
def status():
    return "Clara está funcionando! 😊"
