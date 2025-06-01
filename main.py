from flask import Flask, request
import requests

app = Flask(__name__)

# Substitua abaixo com os dados da sua instância Z-API
ID_INSTANCIA = '3E205CFA4533E06D42D3C'
TOKEN = '23517734C6D44D8122B05'

@app.route("/", methods=["POST"])
def receber_mensagem():
    dados = request.json

    if not dados:
        return "Sem dados", 400

    mensagem = dados.get("message", {}).get("text", "")
    numero = dados.get("message", {}).get("from", "")

    if mensagem and numero:
        resposta = f"Olá! Você enviou: {mensagem}"

        url = f"https://api.z-api.io/instances/{ID_INSTANCIA}/token/{TOKEN}/send-messages"
        payload = {
            "phone": numero,
            "message": resposta
        }

        headers = {"Content-Type": "application/json"}
        requests.post(url, json=payload, headers=headers)

    return "OK", 200

@app.route("/", methods=["GET"])
def home():
    return "Clara está online!"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
