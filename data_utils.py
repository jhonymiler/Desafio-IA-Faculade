# data_utils.py
import pandas as pd

def load_data(file_path='./dados/arrecadacao-estado.csv'):
    df = pd.read_csv(file_path, sep=';')
    df['Ano'] = pd.to_numeric(df['Ano'], errors='coerce')
    numeric_cols = [col for col in df.columns if col not in ['Ano', 'Mês', 'UF']]
    df[numeric_cols] = df[numeric_cols].apply(pd.to_numeric, errors='coerce')
    return df

def format_number(number):
    return f"{number:,.2f}".replace(".", "#").replace(",", ".").replace("#", ",")

def format_number_extended(number):
    abs_number = abs(number)
    if abs_number >= 1e12:
        value = number / 1e12
        label = "trilhão" if value == 1 else "trilhões"
        return f"{value:,.2f} {label}".replace(".", "#").replace(",", ".").replace("#", ",")
    elif abs_number >= 1e9:
        value = number / 1e9
        label = "bilhão" if value == 1 else "bilhões"
        return f"{value:,.2f} {label}".replace(".", "#").replace(",", ".").replace("#", ",")
    elif abs_number >= 1e6:
        value = number / 1e6
        label = "milhão" if value == 1 else "milhões"
        return f"{value:,.2f} {label}".replace(".", "#").replace(",", ".").replace("#", ",")
    else:
        return format_number(number)


def query_categoria(df, ano_inicio, ano_fim, cols, categoria):
    df_cat = df[(df['Ano'] >= ano_inicio) & (df['Ano'] <= ano_fim)].copy()
    
    unique_cols = list(dict.fromkeys(cols))
    df_cat[unique_cols] = df_cat[unique_cols].clip(lower=0)

    total = df_cat[unique_cols].sum().sum()
    estados = df_cat.groupby("UF")[unique_cols].sum().sum(axis=1)
    estado_max = estados.idxmax()
    perc_estado_max = round(estados[estado_max] * 100 / total, 2) if total > 0 else 0.0
    
    df_group = df_cat.groupby(['Ano', 'UF'])[unique_cols].sum()
    df_group = df_group.sum(axis=1).reset_index(name='valor')
    pivot = df_group.pivot(index='Ano', columns='UF', values='valor').fillna(0)
    
    return {
        "categoria": categoria,
        "total": format_number_extended(total),
        "estado_maior_arrecadacao": estado_max,
        "porcentagem": perc_estado_max,
        "anos": pivot.index.tolist(),
        "series": {uf: pivot[uf].tolist() for uf in pivot.columns}
    }

def query_impostos(df, ano_inicio, ano_fim):
    cols_federal = [
        "IMPOSTO SOBRE IMPORTAÇÃO",
        "IMPOSTO SOBRE EXPORTAÇÃO",
        "IPI - FUMO",
        "IPI - BEBIDAS",
        "IPI - AUTOMÓVEIS",
        "IPI - VINCULADO À IMPORTACAO",
        "IPI - OUTROS",
        "IRPF",
        "IRPJ - ENTIDADES FINANCEIRAS",
        "IRPJ - DEMAIS EMPRESAS",
        "IRRF - RENDIMENTOS DO TRABALHO",
        "IRRF - RENDIMENTOS DO CAPITAL",
        "IRRF - REMESSAS P/ EXTERIOR",
        "IRRF - OUTROS RENDIMENTOS",
        "IMPOSTO S/ OPERAÇÕES FINANCEIRAS",
        "IMPOSTO TERRITORIAL RURAL",
        "IMPOSTO PROVIS.S/ MOVIMENT. FINANC. - IPMF",
        "CPMF",
        "CIDE-COMBUSTÍVEIS (parc. não dedutível)",
        "CIDE-COMBUSTÍVEIS",
        "RETENÇÃO NA FONTE - LEI 10.833, Art. 30",
        "PAGAMENTO UNIFICADO"
    ]
    
    cols_social = [
        "COFINS",
        "COFINS - FINANCEIRAS",
        "COFINS - DEMAIS",
        "CONTRIBUIÇÃO PARA O PIS/PASEP",
        "CONTRIBUIÇÃO PARA O PIS/PASEP - FINANCEIRAS",
        "CONTRIBUIÇÃO PARA O PIS/PASEP - DEMAIS",
        "CSLL",
        "CSLL - FINANCEIRAS",
        "CSLL - DEMAIS",
        "CONTRIBUIÇÃO PLANO SEG. SOC. SERVIDORES",
        "CPSSS - Contrib. p/ o Plano de Segurid. Social Serv. Público",
        "CONTRIBUICÕES PARA FUNDAF"
    ]
    
    cols_prev = [
        "RECEITA PREVIDENCIÁRIA",
        "RECEITA PREVIDENCIÁRIA - PRÓPRIA",
        "RECEITA PREVIDENCIÁRIA - DEMAIS",
        "ADMINISTRADAS POR OUTROS ÓRGÃOS"
    ]
    
    cols_impor_export = [
        "IMPOSTO SOBRE IMPORTAÇÃO",
        "IMPOSTO SOBRE EXPORTAÇÃO",
        "IPI - FUMO",
        "IPI - BEBIDAS",
        "IPI - AUTOMÓVEIS",
        "IPI - VINCULADO À IMPORTACAO",
        "IPI - OUTROS"
    ]

    return [
        query_categoria(df, ano_inicio, ano_fim, cols_federal + cols_social + cols_prev + cols_impor_export, "Total Geral"),
        query_categoria(df, ano_inicio, ano_fim, cols_impor_export, "Importação/Exportação"),
        query_categoria(df, ano_inicio, ano_fim, cols_federal, "Imp. Federais"),
        query_categoria(df, ano_inicio, ano_fim, cols_social, "Contribuições Sociais"),
        query_categoria(df, ano_inicio, ano_fim, cols_prev, "Previdência")
    ]

def query_ipi(df, ano_inicio, ano_fim):
    cols_ipi = [
        "IPI - FUMO",
        "IPI - BEBIDAS",
        "IPI - AUTOMÓVEIS",
        "IPI - VINCULADO À IMPORTACAO",
        "IPI - OUTROS"
    ]
    return query_categoria(df, ano_inicio, ano_fim, cols_ipi, "IPI")

def query_cpmf(df, ano_inicio, ano_fim):
    return query_categoria(df, ano_inicio, ano_fim, ["CPMF"], "CPMF")

def query_top5_irpf_irpj_csll(df, ano_inicio, ano_fim):
    df_period = df[(df['Ano'] >= ano_inicio) & (df['Ano'] <= ano_fim)].copy()
    
    cols = ["IRPF", "IRPJ - ENTIDADES FINANCEIRAS", "IRPJ - DEMAIS EMPRESAS",
            "CSLL", "CSLL - FINANCEIRAS", "CSLL - DEMAIS"]
    
    grouped = df_period.groupby("UF")[cols].sum()
    grouped["IRPJ"] = grouped["IRPJ - ENTIDADES FINANCEIRAS"] + grouped["IRPJ - DEMAIS EMPRESAS"]
    grouped["CSLL_total"] = grouped["CSLL"] + grouped["CSLL - FINANCEIRAS"] + grouped["CSLL - DEMAIS"]
    grouped["total"] = grouped["IRPF"] + grouped["IRPJ"] + grouped["CSLL_total"]
    
    top5 = grouped.sort_values("total", ascending=False).head(5)
    categorias = top5.index.tolist()
    
    series = [
        {"name": "IRPF", "data": top5["IRPF"].tolist()},
        {"name": "IRPJ", "data": top5["IRPJ"].tolist()},
        {"name": "CSLL", "data": top5["CSLL_total"].tolist()}
    ]
    return {"categorias": categorias, "series": series}

def query_csll_por_estado(df, ano_inicio, ano_fim):
    df_period = df[(df['Ano'] >= ano_inicio) & (df['Ano'] <= ano_fim)].copy()
    cols = ["CSLL", "CSLL - FINANCEIRAS", "CSLL - DEMAIS"]
    grouped = df_period.groupby("UF")[cols].sum()
    grouped["total"] = grouped.sum(axis=1)

    top5 = grouped.sort_values("total", ascending=False).head(5)
    categorias = top5.index.tolist()

    series = [
        {"name": "CSLL", "data": top5["CSLL"].tolist()},
        {"name": "CSLL - FINANCEIRAS", "data": top5["CSLL - FINANCEIRAS"].tolist()},
        {"name": "CSLL - DEMAIS", "data": top5["CSLL - DEMAIS"].tolist()},
    ]
    return {"categorias": categorias, "series": series}

def query_irpf_sp(df):
    df_sp = df[df['UF'] == "SP"]
    return df_sp.groupby("Ano")["IRPF"].sum().idxmax()

def query_cofins(df):
    df_cof = df[df['Ano'] == 2023]
    total = df_cof["COFINS"].sum()
    financ = df_cof["COFINS - FINANCEIRAS"].sum()
    demais = df_cof["COFINS - DEMAIS"].sum()
    return total, financ, demais

def query_export(df):
    df_exp = df[(df['Ano'] >= 2000) & (df['Ano'] <= 2024) & (df['UF'].isin(["MT", "GO"]))]
    return df_exp.groupby(["UF", "Ano"])["IMPOSTO SOBRE EXPORTAÇÃO"].sum().unstack(fill_value=0).to_dict()

def query_auto(df):
    df_auto = df[df['Ano'] == 2022]
    return df_auto.groupby("UF")["IPI - AUTOMÓVEIS"].sum().to_dict()

def query_irpj(df):
    df_irpj = df[(df['UF'] == "SP") & (df['Ano'] >= 2000) & (df['Ano'] <= 2023)]
    fin = df_irpj.groupby("Ano")["IRPJ - ENTIDADES FINANCEIRAS"].sum().to_dict()
    dem = df_irpj.groupby("Ano")["IRPJ - DEMAIS EMPRESAS"].sum().to_dict()
    return fin, dem

def query_csll(df):
    df_csll = df[(df['Ano'] >= 2000) & (df['Ano'] <= 2023)]
    fin = df_csll.groupby("Ano")["CSLL - FINANCEIRAS"].sum().to_dict()
    nao = df_csll.groupby("Ano")["CSLL - DEMAIS"].sum().to_dict()
    return fin, nao

def query_growth(df):
    df_post = df[df['Ano'] > 2007]
    growth = {}
    cols = [col for col in df.columns if col not in ["Ano", "Mês", "UF", "CPMF"]]
    for col in cols:
        series = df_post.groupby("Ano")[col].sum().sort_index()
        if len(series) > 1 and series.iloc[0] != 0:
            growth[col] = (series.iloc[-1] - series.iloc[0]) / series.iloc[0]
    return max(growth, key=growth.get) if growth else None

###############################################################################
# NOVAS FUNÇÕES (exemplos)
###############################################################################

def query_total_por_mes(df, ano, uf=None):
    """Soma de todas as colunas numéricas, mês a mês, opcionalmente filtrando UF."""
    df_filt = df[df['Ano'] == ano].copy()
    if uf:
        df_filt = df_filt[df_filt['UF'] == uf]
    numeric_cols = [c for c in df_filt.columns if c not in ['Ano','Mês','UF']]
    df_filt[numeric_cols] = df_filt[numeric_cols].clip(lower=0)
    df_filt['soma_mes'] = df_filt[numeric_cols].sum(axis=1)
    resumo = df_filt.groupby('Mês')['soma_mes'].sum()
    return resumo.to_dict()

def query_ranking_estados_ano(df, ano, col):
    """Ranking dos estados para uma coluna específica em um determinado ano."""
    df_filt = df[df['Ano'] == ano].copy()
    df_filt[col] = df_filt[col].clip(lower=0)
    ranking = df_filt.groupby('UF')[col].sum().sort_values(ascending=False)
    return ranking.to_dict()

def query_percentual_uf_ano(df, ano, uf, col):
    """Percentual de um estado em relação ao total do Brasil para uma dada coluna e ano."""
    df_filt = df[df['Ano'] == ano].copy()
    df_filt[col] = df_filt[col].clip(lower=0)
    total_brasil = df_filt[col].sum()
    total_uf = df_filt[df_filt['UF'] == uf][col].sum()
    if total_brasil == 0:
        return 0.0
    return round(100 * total_uf / total_brasil, 2)

def query_colunas_livres(df, ano_inicio, ano_fim, colunas):
    """Soma de colunas específicas, no período, por UF."""
    df_filt = df[(df['Ano'] >= ano_inicio) & (df['Ano'] <= ano_fim)].copy()
    df_filt[colunas] = df_filt[colunas].clip(lower=0)
    group_sum = df_filt.groupby('UF')[colunas].sum()
    # Retorna total por UF e total geral
    total_geral = group_sum.sum().sum()
    return {
        "por_uf": group_sum.to_dict('index'),
        "total_geral": total_geral
    }
