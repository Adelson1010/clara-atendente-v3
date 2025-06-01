from flask import Flask, request, jsonify
import openai
import os

app = Flask(__name__)

# Chave da API da OpenAI (vinda das variáveis de ambiente)
openai.api_key = os.getenv("OPENAI_API_KEY")

@app.route("/", methods=["GET"])
def home():
    return "Clara está ativa!"

@app.route("/", methods=["POST"])
def receber_mensagem():
    try:
        data = request.get_json()

        mensagem = data.get("message", {}).get("text", "")
        telefone = data.get("phone", "")

        if not mensagem or not telefone:
            return jsonify({"status": "erro", "detalhe": "mensagem ou telefone ausente"}), 400

        resposta = gerar_resposta(mensagem)

        enviar_resposta(telefone, resposta)

        return jsonify({"status": "sucesso", "mensagem": "resposta enviada"})
    
    except Exception as e:
        return jsonify({"status": "erro", "detalhe": str(e)}), 500

def gerar_resposta(pergunta):
    resposta = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "Você é Clara, uma atendente virtual simpática e eficiente da CentralPsi. Responda com leveza e clareza."},
            {"role": "user", "content": pergunta}
        ]
    )
    return resposta.choices[0].message["content"]

def enviar_resposta(telefone, mensagem):
    import requests
    url = "https://api.z-api.io/instances/3E205CFA4533E06D42D3C6E882E8CF29/token/23517734C6D44D8122B05660/send-messages"
    payload = {
        "phone": telefone,
        "message": {
            "text": mensagem,
            "type": "chat"
        }
    }
    headers = {"Content-Type": "application/json"}
    requests.post(url, json=payload, headers=headers)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
