from flask import Flask, request, jsonify
from flask_cors import CORS
import openai
import os

app = Flask(__name__)
CORS(app)

# Usa a variável de ambiente com a chave secreta da OpenAI
openai.api_key = os.getenv("OPENAI_API_KEY")

@app.route("/", methods=["GET"])
def home():
    return "Clara está online!", 200

@app.route("/", methods=["POST"])
def receber_mensagem():
    try:
        dados = request.get_json()
        texto_usuario = dados["message"]["text"]
        numero = dados["phone"]

        print(f"Mensagem recebida de {numero}: {texto_usuario}")

        resposta = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Você é a Clara, uma atendente virtual empática e inteligente da CentralPsi. Responda com leveza, gentileza e clareza."},
                {"role": "user", "content": texto_usuario}
            ]
        )

        mensagem_resposta = resposta.choices[0].message["content"].strip()

        return jsonify({
            "replier": {
                "message": {
                    "text": mensagem_resposta,
                    "type": "chat"
                }
            }
        }), 200

    except Exception as e:
        print(f"Erro: {str(e)}")
        return jsonify({"error": "Erro ao processar a mensagem."}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
