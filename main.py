from flask import Flask, request
import requests
import os
import openai

app = Flask(__name__)

openai.api_key = os.getenv("OPENAI_API_KEY")

ZAPI_TOKEN = "23517734C6D44D8122B05660"
ZAPI_INSTANCE = "3E205CFA4533E06D42D3C6E882E8CF29"
ZAPI_URL = f"https://api.z-api.io/instances/{ZAPI_INSTANCE}/token/{ZAPI_TOKEN}/send-messages"

@app.route("/", methods=["POST"])
def responder():
    data = request.get_json()

    if data.get("type") == "message":
        mensagem = data["message"]["text"]
        telefone = data["phone"]

        print(f"Mensagem recebida de {telefone}: {mensagem}")

        # Enviar a pergunta para o ChatGPT
        resposta = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Você é Clara, uma atendente virtual simpática da clínica CentralPsi."},
                {"role": "user", "content": mensagem}
            ]
        )

        texto_resposta = resposta["choices"][0]["message"]["content"]

        # Enviar a resposta via Z-API
        payload = {
            "phone": telefone,
            "message": texto_resposta
        }

        headers = {"Content-Type": "application/json"}
        requests.post(ZAPI_URL, json=payload, headers=headers)

    return "OK", 200

if __name__ == "__main__":
    app.run(debug=True)
