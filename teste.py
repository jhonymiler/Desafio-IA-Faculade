import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def load_data(file_path='./dados/arrecadacao-estado.csv'):
    df = pd.read_csv(file_path, sep=';')
    df['Ano'] = pd.to_numeric(df['Ano'], errors='coerce')
    numeric_cols = [col for col in df.columns if col not in ['Ano', 'Mês', 'UF']]
    df[numeric_cols] = df[numeric_cols].apply(pd.to_numeric, errors='coerce')
    return df

df = load_data()

# =============================================================================
# 1. Imposto sobre Importação (2000-2024)
# =============================================================================
mask_2000_2024 = (df['Ano'] >= 2000) & (df['Ano'] <= 2024)
df_2000_2024 = df[mask_2000_2024]

imp_importacao = df_2000_2024.groupby('UF')['IMPOSTO SOBRE IMPORTAÇÃO'].sum().reset_index()
top_import = imp_importacao.sort_values(by='IMPOSTO SOBRE IMPORTAÇÃO', ascending=False).iloc[0]

print("1. Imposto sobre Importação (2000-2024)")
print("   Estado com maior arrecadação:", top_import['UF'])
print("   Valor total arrecadado: R$", top_import['IMPOSTO SOBRE IMPORTAÇÃO'])
print()

# =============================================================================
# 2. CPMF (2000-2007 – período disponível para análise)
# =============================================================================
mask_cpmf = (df['Ano'] >= 2000) & (df['Ano'] <= 2007)
df_cpmf = df[mask_cpmf]

cpmf_sum = df_cpmf.groupby('UF')['CPMF'].sum().reset_index()
top_cpmf = cpmf_sum.sort_values(by='CPMF', ascending=False).iloc[0]

print("2. CPMF (2000-2007)")
print("   Estado com maior arrecadação de CPMF:", top_cpmf['UF'])
print("   Valor total arrecadado: R$", top_cpmf['CPMF'])
print()

# =============================================================================
# 3. IRPF em São Paulo – Ano de maior arrecadação
# =============================================================================
df_sp = df[df['UF'] == 'SP']
irpf_sp = df_sp.groupby('Ano')['IRPF'].sum().reset_index()
max_irpf = irpf_sp.loc[irpf_sp['IRPF'].idxmax()]

print("3. IRPF em São Paulo")
print("   Ano de maior arrecadação:", int(max_irpf['Ano']))
print("   Valor arrecadado: R$", max_irpf['IRPF'])
print()

# =============================================================================
# 4. COFINS em 2023 – Contribuição de Entidades Financeiras vs. Demais Empresas
# =============================================================================
df_2023 = df[df['Ano'] == 2023]
cofins_fin = df_2023['COFINS - FINANCEIRAS'].sum()
cofins_demais = df_2023['COFINS - DEMAIS'].sum()
total_cofins = cofins_fin + cofins_demais

print("4. COFINS em 2023")
print("   Total COFINS: R$", total_cofins)
print("   - Entidades Financeiras: R$", cofins_fin)
print("   - Demais Empresas: R$", cofins_demais)
print()

# =============================================================================
# 5. Imposto sobre Exportação em MT e GO – Variação ao longo dos anos
# =============================================================================
df_mt_go = df[df['UF'].isin(['MT', 'GO'])]
export_yearly = df_mt_go.groupby(['Ano', 'UF'])['IMPOSTO SOBRE EXPORTAÇÃO'].sum().reset_index()

plt.figure(figsize=(10,6))
sns.lineplot(data=export_yearly, x='Ano', y='IMPOSTO SOBRE EXPORTAÇÃO', hue='UF', marker='o')
plt.title("Exportação – Mato Grosso vs. Goiás (Anual)")
plt.ylabel("Valor Arrecadado (R$)")
plt.tight_layout()
plt.show()

# =============================================================================
# 6. Impostos sobre Automóveis em 2022 – Arrecadação por Estado
# =============================================================================
df_2022 = df[df['Ano'] == 2022]
auto_sum = df_2022.groupby('UF')['IPI - AUTOMÓVEIS'].sum().reset_index()
auto_sum_sorted = auto_sum.sort_values(by='IPI - AUTOMÓVEIS', ascending=False)

print("6. Impostos sobre Automóveis (2022)")
print(auto_sum_sorted)
print()
# Comentário: Estados com maior atividade econômica e frota veicular tendem a arrecadar mais.

# =============================================================================
# 7. IRPJ em SP (2000-2023) – Comparação entre Entidades Financeiras e Demais Empresas
# =============================================================================
df_sp_period = df[(df['UF'] == 'SP') & (df['Ano'] >= 2000) & (df['Ano'] <= 2023)]
irpj_sp = df_sp_period.groupby('Ano').agg({
    'IRPJ - ENTIDADES FINANCEIRAS': 'sum',
    'IRPJ - DEMAIS EMPRESAS': 'sum'
}).reset_index()

plt.figure(figsize=(10,6))
sns.lineplot(data=irpj_sp, x='Ano', y='IRPJ - ENTIDADES FINANCEIRAS', marker='o', label='Entidades Financeiras')
sns.lineplot(data=irpj_sp, x='Ano', y='IRPJ - DEMAIS EMPRESAS', marker='o', label='Demais Empresas')
plt.title("IRPJ em SP (2000-2023)")
plt.ylabel("Valor Arrecadado (R$)")
plt.legend()
plt.tight_layout()
plt.show()

# =============================================================================
# 8. IPI (2000-2024) – Estado com maior arrecadação e principal produto
# =============================================================================
ipi_cols = ['IPI - FUMO', 'IPI - BEBIDAS', 'IPI - AUTOMÓVEIS', 'IPI - VINCULADO À IMPORTACAO', 'IPI - OUTROS']
ipi_sum = df_2000_2024.groupby('UF')[ipi_cols].sum()
ipi_sum['Total_IPI'] = ipi_sum.sum(axis=1)
top_ipi = ipi_sum.sort_values(by='Total_IPI', ascending=False).iloc[0]

print("8. IPI (2000-2024)")
print("   Estado com maior arrecadação de IPI:", top_ipi.name)
print("   Valor total arrecadado: R$", top_ipi['Total_IPI'])
produto_principal = top_ipi[ipi_cols].idxmax()
print("   Principal produto responsável:", produto_principal)
print()

# =============================================================================
# 9. Evolução da CSLL (2004-2023) – Entidades Financeiras vs. Demais Empresas
# =============================================================================
df_2004_2023 = df[(df['Ano'] >= 2004) & (df['Ano'] <= 2023)]
csll_yearly = df_2004_2023.groupby('Ano').agg({
    'CSLL - FINANCEIRAS': 'sum',
    'CSLL - DEMAIS': 'sum'
}).reset_index()

plt.figure(figsize=(10,6))
sns.lineplot(data=csll_yearly, x='Ano', y='CSLL - FINANCEIRAS', marker='o', label='Entidades Financeiras')
sns.lineplot(data=csll_yearly, x='Ano', y='CSLL - DEMAIS', marker='o', label='Demais Empresas')
plt.title("Evolução da CSLL (2004-2023)")
plt.ylabel("Valor Arrecadado (R$)")
plt.legend()
plt.tight_layout()
plt.show()

# =============================================================================
# 10. Desafio Avançado – Imposto/Contribuição com maior crescimento pós-CPMF (2008-2023)
# =============================================================================
df_2008_2023 = df[(df['Ano'] >= 2008) & (df['Ano'] <= 2023)]
annual = df_2008_2023.groupby('Ano').agg({
    'IRPF': 'sum',
    'IRPJ - ENTIDADES FINANCEIRAS': 'sum',
    'IRPJ - DEMAIS EMPRESAS': 'sum',
    'COFINS - FINANCEIRAS': 'sum',
    'COFINS - DEMAIS': 'sum',
    **{col: 'sum' for col in ipi_cols},
    'CSLL - FINANCEIRAS': 'sum',
    'CSLL - DEMAIS': 'sum'
}).reset_index()

annual['IRPJ_Total'] = annual['IRPJ - ENTIDADES FINANCEIRAS'] + annual['IRPJ - DEMAIS EMPRESAS']
annual['COFINS_Total'] = annual['COFINS - FINANCEIRAS'] + annual['COFINS - DEMAIS']
annual['IPI_Total'] = annual[ipi_cols].sum(axis=1)
annual['CSLL_Total'] = annual['CSLL - FINANCEIRAS'] + annual['CSLL - DEMAIS']

def growth_rate(series):
    first = series.iloc[0]
    last = series.iloc[-1]
    return (last - first) / first if first != 0 else None

growth_rates = {
    'IRPF': growth_rate(annual['IRPF']),
    'IRPJ_Total': growth_rate(annual['IRPJ_Total']),
    'COFINS_Total': growth_rate(annual['COFINS_Total']),
    'IPI_Total': growth_rate(annual['IPI_Total']),
    'CSLL_Total': growth_rate(annual['CSLL_Total'])
}

print("10. Crescimento relativo (2008-2023):")
for tax, rate in growth_rates.items():
    print(f"   {tax}: {rate:.2%}")

max_growth_tax = max(growth_rates, key=growth_rates.get)
print("   Imposto/Contribuição que mais cresceu:", max_growth_tax)
print()

# =============================================================================
# Gráficos Sugeridos
# =============================================================================

# Gráfico A: Linha da evolução da CPMF por estado (todos os anos)
cpmf_estado = df.groupby(['Ano', 'UF'])['CPMF'].sum().reset_index()
plt.figure(figsize=(12,8))
sns.lineplot(data=cpmf_estado, x='Ano', y='CPMF', hue='UF', marker='o')
plt.title("Evolução da CPMF por Estado")
plt.ylabel("CPMF (R$)")
plt.tight_layout()
plt.show()

# Gráfico B: Barras empilhadas de IRPF, IRPJ e CSLL em 2023 (top 5 estados)
df_2023['IRPJ_Total'] = df_2023['IRPJ - ENTIDADES FINANCEIRAS'] + df_2023['IRPJ - DEMAIS EMPRESAS']
df_2023['CSLL_Total'] = df_2023.apply(lambda r: r['CSLL - FINANCEIRAS'] + r['CSLL - DEMAIS'] if pd.notnull(r['CSLL - FINANCEIRAS']) else r['CSLL'], axis=1)
state_revenues = df_2023.groupby('UF').agg({
    'IRPF': 'sum',
    'IRPJ_Total': 'sum',
    'CSLL_Total': 'sum'
}).reset_index()
top5_states = state_revenues.sort_values(by='IRPF', ascending=False).head(5)

plt.figure(figsize=(10,6))
plt.bar(top5_states['UF'], top5_states['IRPF'], label='IRPF')
plt.bar(top5_states['UF'], top5_states['IRPJ_Total'], bottom=top5_states['IRPF'], label='IRPJ')
plt.bar(top5_states['UF'], top5_states['CSLL_Total'], bottom=top5_states['IRPF']+top5_states['IRPJ_Total'], label='CSLL')
plt.title("IRPF, IRPJ e CSLL em 2023 (Top 5 Estados)")
plt.ylabel("Valor Arrecadado (R$)")
plt.legend()
plt.tight_layout()
plt.show()

# Gráfico C: Linha múltipla (já gerado na Questão 5 para exportação em MT e GO)

# Gráfico D: Mapa de calor da arrecadação total por estado em 2023
num_cols = df_2023.select_dtypes(include='number').columns.tolist()
# Excluindo colunas que não representam receitas
num_cols = [col for col in num_cols if col not in ['Ano', 'Mês']]
total_2023 = df_2023.groupby('UF')[num_cols].sum().sum(axis=1).reset_index(name='Total')
plt.figure(figsize=(8,6))
sns.heatmap(total_2023.set_index('UF'), annot=True, cmap="YlGnBu")
plt.title("Mapa de Calor: Arrecadação Total por Estado em 2023")
plt.tight_layout()
plt.show()

# Gráfico E: Pizza com participação dos principais impostos em 2023
taxes = ['IRPF', 'IRPJ - ENTIDADES FINANCEIRAS', 'IRPJ - DEMAIS EMPRESAS', 'CPMF', 'COFINS - FINANCEIRAS', 'COFINS - DEMAIS']
tax_values = df_2023[taxes].sum()
plt.figure(figsize=(8,8))
plt.pie(tax_values, labels=tax_values.index, autopct='%1.1f%%', startangle=140)
plt.title("Participação de Impostos em 2023")
plt.tight_layout()
plt.show()

# Gráfico F: Barras simples – Impostos sobre Automóveis (Top 5 estados, 2022)
top5_auto = auto_sum_sorted.head(5)
plt.figure(figsize=(10,6))
sns.barplot(data=top5_auto, x='UF', y='IPI - AUTOMÓVEIS')
plt.title("Impostos sobre Automóveis (Top 5 Estados) - 2022")
plt.ylabel("Valor Arrecadado (R$)")
plt.tight_layout()
plt.show()

# Gráfico G: (Desafio) Gráfico de barras horizontais – CSLL em 2023 por estado
csll_state = df_2023.groupby('UF').agg({
    'CSLL - FINANCEIRAS': 'sum',
    'CSLL - DEMAIS': 'sum'
}).reset_index().sort_values(by='CSLL - FINANCEIRAS', ascending=False)
plt.figure(figsize=(10,6))
plt.barh(csll_state['UF'], csll_state['CSLL - FINANCEIRAS'], color='orange', label='Financeiras')
plt.barh(csll_state['UF'], csll_state['CSLL - DEMAIS'], left=csll_state['CSLL - FINANCEIRAS'], color='green', label='Demais')
plt.xlabel("Valor Arrecadado (R$)")
plt.title("CSLL em 2023 por Estado")
plt.legend()
plt.tight_layout()
plt.show()

# =============================================================================
# Análises Adicionais
# =============================================================================
# Exemplo: Tendência da arrecadação total (soma de impostos principais) ao longo dos anos
impostos_principais = ['IMPOSTO SOBRE IMPORTAÇÃO', 'IMPOSTO SOBRE EXPORTAÇÃO', 'IRPF',
                       'IRPJ - ENTIDADES FINANCEIRAS', 'IRPJ - DEMAIS EMPRESAS', 'CPMF']
df['Total_Principal'] = df[impostos_principais].sum(axis=1)
total_annual = df.groupby('Ano')['Total_Principal'].sum().reset_index()

plt.figure(figsize=(10,6))
sns.lineplot(data=total_annual, x='Ano', y='Total_Principal', marker='o')
plt.title("Tendência da Arrecadação Total (Principais Impostos)")
plt.ylabel("Valor Arrecadado (R$)")
plt.tight_layout()
plt.show()
