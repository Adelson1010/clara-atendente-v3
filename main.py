from flask import Flask, request
import requests
import os

app = Flask(__name__)

ZAPI_TOKEN = os.getenv("ZAPI_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

@app.route("/")
def home():
    return "Clara está online!"

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.get_json()
    try:
        message = data["message"]
        sender = data["sender"]["id"]
        print(f"Mensagem recebida de {sender}: {message}")

        # Gera resposta com OpenAI
        openai_response = requests.post(
            "https://api.openai.com/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {OPENAI_API_KEY}",
                "Content-Type": "application/json"
            },
            json={
                "model": "gpt-3.5-turbo",
                "messages": [
                    {"role": "system", "content": "Você é Clara, uma assistente simpática da CentralPsi. Seja breve, humana e acolhedora."},
                    {"role": "user", "content": message}
                ]
            }
        )

        resposta = openai_response.json()["choices"][0]["message"]["content"]

        # Envia resposta para o WhatsApp via Z-API
        zapi_url = f"https://api.z-api.io/instances/claratest01/token/{ZAPI_TOKEN}/send-text"
        requests.post(
            zapi_url,
            json={
                "phone": sender,
                "message": resposta
            }
        )

        return {"status": "mensagem enviada"}, 200

    except Exception as e:
        print("Erro:", e)
        return {"erro": str(e)}, 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
