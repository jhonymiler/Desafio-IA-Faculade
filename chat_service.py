# chat_service.py
import asyncio
from langchain_core.messages import SystemMessage, HumanMessage
from agent_service import create_agent

# Cria o agente (singleton)
agent = create_agent()

async def get_reply(conversa) -> str:
    try:
        # agent.run() é síncrono; se ocorrer erro, captura e retorna uma mensagem
        return agent.run(conversa)
    except Exception as e:
        return f"Erro ao processar a consulta: {e}"

def generate_conversation(user_message: str, system_context: str):
    return [
        SystemMessage(content=system_context),
        HumanMessage(content=user_message)
    ]

def build_system_prompt(user_message: str) -> str:
    # Instruções do sistema para garantir respostas em português
    return (
        "Você é um assistente especializado em dados fiscais do Brasil. "
        "Responda exclusivamente em português, de forma clara e objetiva, "
        "utilizando os recursos disponíveis para retornar dados precisos. "
        "Caso não seja possível obter todas as informações, informe o que falta. "
        f"Usuário: {user_message}"
    )
