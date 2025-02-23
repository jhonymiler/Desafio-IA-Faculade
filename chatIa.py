from flask import render_template, request, jsonify, session
from app import app
from dotenv import load_dotenv
import asyncio
from chat_service import get_reply, generate_conversation
import os

load_dotenv()
app.secret_key = os.urandom(24)

@app.route('/chat_ia')
def chat_ia():
    # Inicia ou limpa o histórico da sessão
    session['conversation_history'] = []
    context = {
        "title": "CHAT IA",
        "subTitle": "Análise feita por inteligência artificial"
    }
    return render_template("chatIa.html", **context)

@app.route('/send_message', methods=['POST'])
def send_message():
    data = request.get_json()
    user_message = data.get("message", "")
    user_apikey = data.get("apikey", "").strip()

    # Recupera ou inicializa o histórico sem incluir o prompt do sistema
    if 'conversation_history' not in session:
        session['conversation_history'] = []
    history = session['conversation_history']
    
    # Adiciona a mensagem do usuário ao histórico
    history.append({"role": "user", "content": user_message})
    session['conversation_history'] = history

    # Gera a conversa sempre com o prompt do sistema no topo
    conversa = generate_conversation(history)

    print(f"Conversa: {conversa}")
    
    try:
        resposta_completa = asyncio.run(get_reply(conversa, api_key=user_apikey))
        history.append({"role": "assistant", "content": resposta_completa})
        session['conversation_history'] = history
    except Exception as e:
        resposta_completa = str(e)
    return jsonify({"reply": resposta_completa})