from flask import Flask, request
import requests

app = Flask(__name__)

@app.route('/')
def home():
    return 'Clara está online!'

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.get_json()
    
    if data and 'message' in data:
        mensagem_recebida = data['message']
        numero = data.get('phone')
        
        if numero and mensagem_recebida:
            resposta = 'Recebido! Em breve, Clara vai te responder.'
            
            requests.post(
                'https://api.z-api.io/instances/3E205CFA4533E06D42D3C/token/23517734C6D44D8122B05/send-messages',
                json={
                    'phone': numero,
                    'message': resposta
                }
            )
    
    return 'OK', 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
