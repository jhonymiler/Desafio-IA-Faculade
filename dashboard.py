from flask import render_template, request
from app import app
import data_utils as du

# Carrega os dados uma única vez
df = du.load_data()

@app.route('/dashboard')
def dash_index():
    ano_inicio = int(request.args.get("ano_inicio", 2000))
    ano_fim = int(request.args.get("ano_fim", 2024))

    state_cpmf = du.query_cpmf(df,2000,2007)
    year_irpf = du.query_irpf_sp(df)
    total_cofins, cofins_fin, cofins_dem = du.query_cofins(df)
    export_data = du.query_export(df)
    auto_by_state = du.query_auto(df)
    irpj_fin, irpj_dem = du.query_irpj(df)
    state_ipi, prod_ipi = du.query_ipi(df)
    csll_fin, csll_nao = du.query_csll(df)
    tax_fast = du.query_growth(df)

    context = {
        "title": "Dashboard",
        "subTitle": "Análise de Impostos",
        "state_cpmf": state_cpmf,
        "year_sp_irpf": year_irpf,
        "total_cofins": total_cofins,
        "cofins_financeiras": cofins_fin,
        "cofins_demais": cofins_dem,
        "export_data": export_data,
        "auto_by_state": auto_by_state,
        "irpj_financeiras": irpj_fin,
        "irpj_demais": irpj_dem,
        "state_ipi": state_ipi,
        "produto_ipi": prod_ipi,
        "csll_financeiras": csll_fin,
        "csll_nao_financeiras": csll_nao,
        "tax_fastest": tax_fast,
    }
    return render_template("teste.html", **context)