from flask import Flask, request
import os
import requests

app = Flask(__name__)

@app.route('/', methods=['GET'])
def home():
    return 'Clara está online!'

@app.route('/', methods=['POST'])
def responder():
    data = request.get_json()

    if not data or 'message' not in data or 'phone' not in data:
        return {'status': 'ignorado'}, 200

    mensagem = data['message']
    numero = data['phone']

    resposta = f"Você disse: {mensagem}"

    requests.post(
        'https://api.z-api.io/instances/SEU_ID_DO_ZAPI/token/SEU_TOKEN_DO_ZAPI/send-messages',
        json={
            'phone': numero,
            'message': resposta
        }
    )

    return {'status': 'enviado'}, 200

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
