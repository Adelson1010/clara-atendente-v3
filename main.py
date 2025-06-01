from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

# Dados da Z-API
ID_INSTANCIA = '3E205CFA4533E06D42D3C6E882E8CF29'
TOKEN_INSTANCIA = '23517734C6D44D8122B05660'
URL_API = f'https://api.z-api.io/instances/{ID_INSTANCIA}/token/{TOKEN_INSTANCIA}/send-messages'

@app.route("/", methods=["GET"])
def home():
    return "Clara está online!"

@app.route("/", methods=["POST"])
def receber_mensagem():
    data = request.json

    # Extrair informações da mensagem
    try:
        numero = data["message"]["from"]
        texto = data["message"]["body"]
    except (KeyError, TypeError):
        return jsonify({"status": "ignorado", "motivo": "mensagem malformada"})

    # Defina a resposta padrão
    resposta = "Olá! Eu sou a Clara, atendente virtual. Como posso te ajudar hoje?"

    # Enviar a resposta
    payload = {
        "phone": numero,
        "message": resposta
    }
    response = requests.post(URL_API, json=payload)

    if response.status_code == 200:
        return jsonify({"status": "ok", "mensagem_enviada": resposta})
    else:
        return jsonify({"status": "erro", "detalhes": response.text}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
