from flask import Flask, request

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def webhook():
    if request.method == 'POST':
        data = request.get_json()
        print("📩 Webhook recebido:")
        print(data)
        return 'Recebido com sucesso', 200
    return 'Clara está online!', 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
