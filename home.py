from flask import render_template, request
from app import app
import data_utils as du

# Carrega os dados uma única vez
df = du.load_data()

@app.route("/")
def index():
    ano_inicio = int(request.args.get("ano_inicio", 2000))
    ano_fim = int(request.args.get("ano_fim", 2024))
    visao_geral = du.query_impostos(df, ano_inicio, ano_fim)

    state_cpmf = du.query_cpmf(df, 2000,2007)

    total_geral = visao_geral[0]
    # Extraímos os valores por estado (espera-se apenas 1 ano, 2023)
    heatmap_data = { uf: sum(valores) for uf, valores in total_geral["series"].items() }
    #soma valores de todos os estados
    valor_total = sum(heatmap_data.values())

    # organize o heatmap por valor do maior para o menor
    heatmap_data = dict(sorted(heatmap_data.items(), key=lambda x: x[1], reverse=True))

    query_top5_irpf_irpj_csll = du.query_top5_irpf_irpj_csll(df, ano_inicio, ano_fim)
    query_csll_por_estado = du.query_csll_por_estado(df, ano_inicio, ano_fim)

    ipi = du.query_ipi(df, ano_inicio, ano_fim)

    context = {
        "title": "Dashboard",
        "subTitle": "CRM",
        "visao_geral": visao_geral,
        "ano_inicio": ano_inicio,
        "ano_fim": ano_fim,
        "state_cpmf": state_cpmf,
        "heatmap_data": heatmap_data,
        "valor_total": valor_total,
        "top5_irpf_irpj_csll": query_top5_irpf_irpj_csll,
        "ipi": ipi,
        "csll_por_estado": query_csll_por_estado
    }
    return render_template("index.html", **context)

