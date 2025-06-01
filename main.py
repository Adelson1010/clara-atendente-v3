from flask import Flask, request
import requests

app = Flask(__name__)

@app.route('/', methods=['GET'])
def home():
    return 'Clara está online!'

@app.route('/', methods=['POST'])
def atender():
    data = request.get_json()

    if not data or 'message' not in data:
        return {'status': 'mensagem vazia'}, 400

    mensagem = data['message']['text']
    numero = data['message']['from']

    if mensagem.strip().lower() == 'oi':
        texto_resposta = 'Olá! Eu sou a Clara, assistente virtual. Como posso ajudar?'
    else:
        texto_resposta = 'Me desculpe, ainda estou aprendendo. Por enquanto, respondo apenas "oi".'

    resposta = {
        "phone": numero,
        "message": texto_resposta
    }

    # Envia a resposta usando a API da Z-API
    requests.post(
        'https://api.z-api.io/instances/3E205CFA4533E06D42D3C/token/23517734C6D44D8122B05/send-text',
        json=resposta
    )

    return {'status': 'mensagem enviada'}, 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
