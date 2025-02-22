import asyncio
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
from agent_service import create_agent

async def get_reply(conversa, api_key: str = None) -> str:
    try:
        agent = create_agent(api_key)
        result = agent.invoke(conversa)  # Executa a consulta com a lista de mensagens
        if isinstance(result, dict) and "output" in result:
            return result["output"]
        elif hasattr(result, "content"):
            return result.content
        else:
            return str(result)
    except Exception as e:
        return f"Erro ao processar a consulta: {e}"
    
def generate_conversation(history):
    system_prompt = (
        "Você é um assistente especializado em dados fiscais do Brasil. Você responde em português brasileiro. "
        "Responda sempre em português, de forma clara e objetiva, utilizando os recursos disponíveis para retornar dados precisos. "
        "Caso não seja possível obter todas as informações, informe o que falta."
    )
    messages = [SystemMessage(content=system_prompt)]
    for msg in history:
        if msg["role"] == "user":
            messages.append(HumanMessage(content=msg["content"]))
        else:
            messages.append(AIMessage(content=msg["content"]))
    return messages