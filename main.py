from flask import Flask, request, jsonify
import openai
import os

app = Flask(__name__)

# Pega a chave da OpenAI a partir das variáveis de ambiente do Render
openai.api_key = os.getenv("OPENAI_API_KEY")

@app.route("/", methods=["GET"])
def home():
    return "Clara está no ar!"

@app.route("/", methods=["POST"])
def receber_mensagem():
    dados = request.json

    if not dados:
        return jsonify({"erro": "Dados JSON ausentes"}), 400

    if dados.get("type") != "message":
        return jsonify({"mensagem": "Evento ignorado"}), 200

    texto_recebido = dados.get("message", {}).get("text", "")
    telefone = dados.get("phone", "")

    if not texto_recebido or not telefone:
        return jsonify({"erro": "Mensagem ou telefone ausente"}), 400

    try:
        resposta = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Você é uma atendente virtual simpática chamada Clara, criada para ajudar de forma leve e eficiente."},
                {"role": "user", "content": texto_recebido}
            ]
        )
        mensagem_clara = resposta.choices[0].message["content"].strip()

        return jsonify({
            "phone": telefone,
            "message": mensagem_clara
        })

    except Exception as e:
        return jsonify({"erro": f"Erro ao gerar resposta: {str(e)}"}), 500

# Código que garante que o Render use a porta correta
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
