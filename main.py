from flask import Flask, request, jsonify
import os
import openai
import requests

app = Flask(__name__)

# Pegando a chave da OpenAI do ambiente
openai.api_key = os.getenv("OPENAI_API_KEY")

# Dados da Z-API
ZAPI_INSTANCE_ID = "3E205CFA4533E06D42D3C6E882E8CF29"
ZAPI_TOKEN = "23517734C6D44D8122B05660"
ZAPI_URL = f"https://api.z-api.io/instances/{ZAPI_INSTANCE_ID}/token/{ZAPI_TOKEN}/send-messages"

@app.route("/", methods=["POST"])
def whatsapp_webhook():
    data = request.json

    try:
        # Pegando o número e a mensagem recebida
        message = data['message']
        number = data['phone']

        # Ignorar mensagens vazias
        if not message:
            return jsonify({"status": "mensagem vazia"}), 200

        # Cria a resposta com a OpenAI
        resposta = gerar_resposta_clara(message)

        # Envia a resposta de volta pelo WhatsApp
        payload = {
            "phone": number,
            "message": resposta
        }

        headers = {"Content-Type": "application/json"}
        requests.post(ZAPI_URL, json=payload, headers=headers)

        return jsonify({"status": "mensagem recebida e respondida"}), 200

    except Exception as e:
        return jsonify({"erro": str(e)}), 500

def gerar_resposta_clara(pergunta):
    prompt = f"Você é Clara, uma atendente virtual simpática e objetiva. Responda de forma clara: {pergunta}"

    resposta = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "Você é uma assistente chamada Clara."},
            {"role": "user", "content": pergunta}
        ],
        temperature=0.7
    )

    return resposta.choices[0].message["content"].strip()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
