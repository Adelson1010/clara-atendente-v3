from flask import Flask, request
import openai
import os

app = Flask(__name__)

# Pegando a chave da OpenAI de uma variável de ambiente
openai.api_key = os.getenv("OPENAI_API_KEY")

@app.route("/", methods=["GET"])
def index():
    return "Clara está online 🎉"

@app.route("/", methods=["POST"])
def webhook():
    data = request.get_json()

    if not data:
        return {"erro": "Requisição sem JSON"}, 400

    if data.get("type") == "message":
        try:
            phone = data["phone"]
            message = data["message"]["text"]
            print(f"Mensagem recebida de {phone}: {message}")

            resposta = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "Você é uma atendente virtual chamada Clara, educada, simpática e eficiente."},
                    {"role": "user", "content": message}
                ]
            )

            resposta_texto = resposta.choices[0].message["content"]

            resposta_final = {
                "phone": phone,
                "text": resposta_texto
            }

            return resposta_final, 200

        except Exception as e:
            print("Erro:", e)
            return {"erro": "Erro interno no servidor"}, 500

    return {"mensagem": "Recebido com sucesso"}, 200

if __name__ == "__main__":
    app.run()
