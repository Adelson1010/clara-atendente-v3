from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

@app.route("/", methods=["POST"])
def receber_mensagem():
    data = request.get_json()
    if data and "message" in data:
        mensagem = data["message"].get("body", "").lower()
        numero = data["message"]["from"]
        
        if "oi" in mensagem:
            responder(numero, "Oi! Aqui é a Clara. Como posso ajudar?")
        elif "horário" in mensagem:
            responder(numero, "Nosso horário de atendimento é das 8h às 18h.")
        else:
            responder(numero, "Desculpe, não entendi. Pode repetir?")
    
    return jsonify({"status": "mensagem recebida"})

def responder(telefone, texto):
    url = "https://api.z-api.io/instances/3E205CFA4533E06D42D3C/token/23517734C6D44D8122B05/send-text"
    payload = {
        "phone": telefone,
        "message": texto
    }
    requests.post(url, json=payload)

@app.route("/", methods=["GET"])
def status():
    return "Clara está online!"
