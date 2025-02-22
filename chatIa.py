# chatIa.py
from flask import render_template, request, jsonify
from app import app
from dotenv import load_dotenv
import asyncio
from chat_service import get_reply, generate_conversation, build_system_prompt

load_dotenv()

@app.route('/chat_ia')
def chat_ia():
    context = {
        "title": "CHAT IA",
        "subTitle": "Análise feita por inteligência artificial"
    }
    return render_template("chatIa.html", **context)

@app.route('/send_message', methods=['POST'])
def send_message():
    data = request.get_json()
    user_message = data.get("message", "")
    system_prompt = build_system_prompt(user_message)
    conversa = generate_conversation(user_message, system_prompt)
    resposta_completa = asyncio.run(get_reply(conversa))
    return jsonify({"reply": resposta_completa})
