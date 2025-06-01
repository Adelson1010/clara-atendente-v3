from flask import Flask, request

app = Flask(__name__)

@app.route("/", methods=["POST"])
def receber_webhook():
    data = request.json
    print("📩 Webhook recebido:", data)
    return "OK", 200

@app.route("/", methods=["GET"])
def home():
    return "Clara está online!", 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
