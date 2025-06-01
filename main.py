from flask import Flask, request, jsonify
import requests
import openai

app = Flask(__name__)

Z_API_TOKEN = "23517734C6D44D8122B05660"
Z_API_INSTANCE_ID = "3E205CFA4533E06D42D3C6E882E8CF29"
OPENAI_API_KEY = "sua-chave-da-openai-aqui"

openai.api_key = OPENAI_API_KEY

@app.route("/", methods=["POST"])
def responder():
    data = request.get_json()

    try:
        if data["type"] == "message":
            mensagem_recebida = data["message"]["text"]
            numero = data["phone"]

            # Gerar resposta da IA
            resposta = gerar_resposta_ia(mensagem_recebida)

            # Enviar mensagem de volta via Z-API
            url = f"https://api.z-api.io/instances/{Z_API_INSTANCE_ID}/token/{Z_API_TOKEN}/send-text"
            payload = {
                "phone": numero,
                "message": resposta
            }
            headers = {"Content-Type": "application/json"}

            r = requests.post(url, json=payload, headers=headers)
            print(f"Enviado para {numero}: {resposta}")
    except Exception as e:
        print("Erro:", e)

    return jsonify({"status": "Recebido com sucesso"}), 200

def gerar_resposta_ia(pergunta):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "Você é uma atendente virtual chamada Clara, gentil e eficiente."},
            {"role": "user", "content": pergunta}
        ]
    )
    return response.choices[0].message.content.strip()

@app.route("/", methods=["GET"])
def verificar():
    return "Clara está online 💬"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
