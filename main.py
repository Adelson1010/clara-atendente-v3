from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

@app.route('/', methods=['GET'])
def home():
    return 'Clara está online!'

@app.route('/', methods=['POST'])
def webhook():
    data = request.get_json()
    print("Recebido:", data)

    # Confirma que é mensagem recebida
    if data and 'message' in data and 'from' in data['message']:
        sender = data['message']['from']  # Número de quem enviou
        url = "https://api.z-api.io/instances/3E205CFA4533E06D42D3C/token/23517734C6D44D8122B05/send-text"

        body = {
            "phone": sender,
            "message": "Oi! Aqui é a Clara, atendente virtual. Como posso te ajudar?"
        }

        r = requests.post(url, json=body)
        print("Resposta da API:", r.text)

    return jsonify({"status": "mensagem recebida"})
