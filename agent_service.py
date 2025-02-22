import re
import os
from langchain.agents import Tool, initialize_agent, AgentType
from langchain_groq import ChatGroq
from data_utils import (
    load_data, query_impostos, query_ipi, query_cpmf,
    query_total_por_mes, query_ranking_estados_ano, query_percentual_uf_ano,
    query_colunas_livres, query_top5_irpf_irpj_csll, query_csll_por_estado,
    query_irpf_sp, query_cofins, query_export, query_auto, query_irpj,
    query_csll, query_growth
)

from dotenv import load_dotenv

# Carrega as variáveis de ambiente do arquivo .env
load_dotenv()

# Carrega o DataFrame globalmente
df = load_data("./dados/arrecadacao-estado.csv")

def small_talk_tool_func(input_str: str) -> str:
    return "Olá! Estou aqui para ajudar com dados fiscais. Por favor, informe sua consulta com detalhes (ex: anos, UF, colunas)."

small_talk_tool = Tool(
    name="SmallTalk",
    func=small_talk_tool_func,
    description="Use esta ferramenta se o usuário estiver apenas cumprimentando ou conversando de forma genérica."
)

def query_impostos_tool_func(input_str: str) -> str:
    try:
        input_str = input_str.replace("'", "").replace('"', "").strip()
        anos = re.findall(r"\d{4}", input_str)
        if len(anos) < 2:
            return "Informe dois anos (ex: '2000 2003')."
        ano_inicio, ano_fim = int(anos[0]), int(anos[1])
        result = query_impostos(df, ano_inicio, ano_fim)
        return str(result)
    except Exception as e:
        return f"Erro ao consultar impostos: {e}"

query_impostos_tool = Tool(
    name="ConsultaImpostos",
    func=query_impostos_tool_func,
    description="Use para consultar impostos gerais entre dois anos (ex: '2000 2003')."
)

def query_ipi_tool_func(input_str: str) -> str:
    try:
        input_str = input_str.replace("'", "").replace('"', "").strip()
        anos = re.findall(r"\d{4}", input_str)
        if len(anos) < 2:
            return "Informe dois anos (ex: '2000 2005')."
        ano_inicio, ano_fim = int(anos[0]), int(anos[1])
        result = query_ipi(df, ano_inicio, ano_fim)
        return str(result)
    except Exception as e:
        return f"Erro ao consultar IPI: {e}"

query_ipi_tool = Tool(
    name="ConsultaIPI",
    func=query_ipi_tool_func,
    description="Use para consultar dados de IPI entre dois anos (ex: '2000 2005')."
)

def query_cpmf_tool_func(input_str: str) -> str:
    try:
        input_str = input_str.replace("'", "").replace('"', "").strip()
        anos = re.findall(r"\d{4}", input_str)
        if len(anos) < 2:
            return "Informe dois anos (ex: '2001 2003')."
        ano_inicio, ano_fim = int(anos[0]), int(anos[1])
        result = query_cpmf(df, ano_inicio, ano_fim)
        return str(result)
    except Exception as e:
        return f"Erro ao consultar CPMF: {e}"

query_cpmf_tool = Tool(
    name="ConsultaCPMF",
    func=query_cpmf_tool_func,
    description="Use para consultar CPMF entre dois anos (ex: '2001 2003')."
)

def query_total_mes_tool_func(input_str: str) -> str:
    try:
        input_str = input_str.replace("'", "").replace('"', "").strip()
        parts = input_str.split()
        if len(parts) < 1:
            return "Informe o ano (e opcionalmente a UF), ex: '2000 SP'."
        ano = int(parts[0].strip())
        uf = parts[1].upper().strip() if len(parts) >= 2 else None
        result = query_total_por_mes(df, ano, uf)
        return str(result)
    except Exception as e:
        return f"Erro ao consultar total por mês: {e}"

query_total_mes_tool = Tool(
    name="ConsultaTotalPorMes",
    func=query_total_mes_tool_func,
    description="Use para consultar o total por mês para um ano (opcionalmente UF). Ex: '2000 SP' ou '2000'."
)

def query_percentual_tool_func(input_str: str) -> str:
    try:
        input_str = input_str.replace("'", "").replace('"', "").strip()
        parts = input_str.split()
        if len(parts) < 3:
            return "Informe: 'ano UF coluna' (ex: '2000 SP IRPF')."
        ano = int(parts[0].strip())
        uf = parts[1].upper().strip()
        col = parts[2].upper().strip()
        pct = query_percentual_uf_ano(df, ano, uf, col)
        return f"{uf} representa {pct}% de {col} no ano {ano}."
    except Exception as e:
        return f"Erro ao calcular percentual: {e}"

query_percentual_tool = Tool(
    name="ConsultaPercentual",
    func=query_percentual_tool_func,
    description="Use para calcular o percentual de um estado para uma coluna em um ano. Ex: '2000 SP IRPF'."
)

def query_colunas_tool_func(input_str: str) -> str:
    try:
        input_str = input_str.replace("'", "").replace('"', "").strip()
        parts = input_str.split()
        if len(parts) < 3:
            return "Informe: 'ano_inicio ano_fim coluna1, coluna2, ...'."
        ano_inicio = int(parts[0].strip())
        ano_fim = int(parts[1].strip())
        cols_str = " ".join(parts[2:])
        colunas = [c.strip() for c in cols_str.split(',')]
        result = query_colunas_livres(df, ano_inicio, ano_fim, colunas)
        return str(result)
    except Exception as e:
        return f"Erro ao consultar colunas: {e}"

query_colunas_tool = Tool(
    name="ConsultaColunasLivres",
    func=query_colunas_tool_func,
    description="Use para somar colunas específicas entre dois anos. Ex: '2000 2005 IRPF, IRPJ - DEMAIS'."
)

def query_top5_tool_func(input_str: str) -> str:
    try:
        input_str = input_str.replace("'", "").replace('"', "").strip()
        anos = re.findall(r"\d{4}", input_str)
        if len(anos) < 2:
            return "Informe dois anos (ex: '2000 2003')."
        ano_inicio, ano_fim = int(anos[0]), int(anos[1])
        result = query_top5_irpf_irpj_csll(df, ano_inicio, ano_fim)
        return str(result)
    except Exception as e:
        return f"Erro ao obter ranking top5: {e}"

query_top5_tool = Tool(
    name="ConsultaTop5IRPFIRPJCSLL",
    func=query_top5_tool_func,
    description="Use para obter o ranking dos 5 estados com maior arrecadação de IRPF, IRPJ e CSLL entre dois anos (ex: '2000 2003')."
)

def query_csll_estado_tool_func(input_str: str) -> str:
    try:
        input_str = input_str.replace("'", "").replace('"', "").strip()
        anos = re.findall(r"\d{4}", input_str)
        if len(anos) < 2:
            return "Informe dois anos (ex: '2000 2003')."
        ano_inicio, ano_fim = int(anos[0]), int(anos[1])
        result = query_csll_por_estado(df, ano_inicio, ano_fim)
        return str(result)
    except Exception as e:
        return f"Erro ao consultar CSLL por estado: {e}"

query_csll_estado_tool = Tool(
    name="ConsultaCSLLPorEstado",
    func=query_csll_estado_tool_func,
    description="Use para consultar CSLL por estado entre dois anos (ex: '2000 2003')."
)

def query_irpf_sp_tool_func(input_str: str) -> str:
    try:
        result = query_irpf_sp(df)
        return f"O ano com maior IRPF em SP é {result}."
    except Exception as e:
        return f"Erro ao identificar o ano com maior IRPF em SP: {e}"

query_irpf_sp_tool = Tool(
    name="ConsultaIRPF_SP",
    func=query_irpf_sp_tool_func,
    description="Use para identificar o ano com maior IRPF em SP."
)

def query_cofins_tool_func(input_str: str) -> str:
    try:
        total, financ, demais = query_cofins(df)
        return f"COFINS 2023: Total={total}, Financeiras={financ}, Demais={demais}."
    except Exception as e:
        return f"Erro ao consultar COFINS: {e}"

query_cofins_tool = Tool(
    name="ConsultaCOFINS",
    func=query_cofins_tool_func,
    description="Use para consultar os totais de COFINS (Financeiras e Demais) para 2023."
)

def query_export_tool_func(input_str: str) -> str:
    try:
        result = query_export(df)
        return str(result)
    except Exception as e:
        return f"Erro ao consultar dados de exportação: {e}"

query_export_tool = Tool(
    name="ConsultaExportacao",
    func=query_export_tool_func,
    description="Use para consultar os dados de exportação para MT e GO entre 2000 e 2024."
)

def query_auto_tool_func(input_str: str) -> str:
    try:
        result = query_auto(df)
        return str(result)
    except Exception as e:
        return f"Erro ao consultar IPI - AUTOMÓVEIS: {e}"

query_auto_tool = Tool(
    name="ConsultaAuto",
    func=query_auto_tool_func,
    description="Use para consultar a soma de IPI - AUTOMÓVEIS para 2022 por estado."
)

def query_irpj_tool_func(input_str: str) -> str:
    try:
        result = query_irpj(df)
        return str(result)
    except Exception as e:
        return f"Erro ao consultar IRPJ: {e}"

query_irpj_tool = Tool(
    name="ConsultaIRPJ",
    func=query_irpj_tool_func,
    description="Use para consultar dados de IRPJ para SP entre 2000 e 2023."
)

def query_csll_tool_func(input_str: str) -> str:
    try:
        result = query_csll(df)
        return str(result)
    except Exception as e:
        return f"Erro ao consultar CSLL: {e}"

query_csll_tool = Tool(
    name="ConsultaCSLL",
    func=query_csll_tool_func,
    description="Use para consultar dados de CSLL para o período 2000-2023."
)

def query_growth_tool_func(input_str: str) -> str:
    try:
        result = query_growth(df)
        if result:
            return f"A coluna com maior crescimento após 2007 é: {result}."
        return "Não foi possível identificar o crescimento."
    except Exception as e:
        return f"Erro ao consultar crescimento: {e}"

query_growth_tool = Tool(
    name="ConsultaGrowth",
    func=query_growth_tool_func,
    description="Use para identificar a coluna com maior crescimento após 2007."
)

def create_agent():
    """Cria um agente ReAct com todas as Tools definidas."""
    api_key = os.getenv("GROQ_API_KEY")
    llm = ChatGroq(model="mixtral-8x7b-32768", temperature=0.1)
    tools = [
        small_talk_tool,
        query_impostos_tool,
        query_ipi_tool,
        query_cpmf_tool,
        query_total_mes_tool,
        query_percentual_tool,
        query_colunas_tool,
        query_top5_tool,
        query_csll_estado_tool,
        query_irpf_sp_tool,
        query_cofins_tool,
        query_export_tool,
        query_auto_tool,
        query_irpj_tool,
        query_csll_tool,
        query_growth_tool
    ]
    # Configura handle_parsing_errors para que o agente tente novamente em caso de erro de parsing
    agent = initialize_agent(
        tools=tools,
        llm=llm,
        agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
        verbose=False,
        handle_parsing_errors=True
    )
    return agent
