# SEÇÃO 1: IMPORTAÇÕES E CONFIGURAÇÕES
import streamlit as st #  para criar aplicações web interativas
import pandas as pd #  para manipulação e análise de dados
import plotly.express as px # para criar gráficos interativos

st.set_page_config(layout="wide") # largura da tela

# --- CARREGAR DADOS ---
df = pd.read_csv(r"C:\Laboratório\dashboard\supermarket_sales.csv", sep=";", decimal=",")

# --- CONVERSÃO DE DATAS ---
df["Date"] = pd.to_datetime(df["Date"])
df = df.sort_values("Date")

# --- FILTRO POR MÊS ---
df["Month"] = df["Date"].dt.to_period('M').astype(str)
month = st.sidebar.selectbox("Mês", df["Month"].unique())
df_filtered = df[df["Month"] == month]

st.title("Dashboard - Visualização da Informação")
st.markdown("Visualizações das três principais unidades: **Temporal, Hierárquica e Geográfica**.")

# --- 1. VISUALIZAÇÃO TEMPORAL ---
st.header("1. Visualização Temporal")

col1, col2, col3 = st.columns(3)

# Gráfico de Linha: Faturamento diário por cidade
# Para cada dia + cada cidade = Soma de todas as vendas daquele dia naquela cidade
fig_line = px.line(
    df_filtered,
    x="Date",
    y="Total",
    color="City",
    title="Linha: Faturamento diário por cidade"
)
col1.plotly_chart(fig_line, use_container_width=True)

# Gráfico de Área: Acúmulo de vendas no mês
# Progresso acumulativo por cidade
df_filtered['Cumulative Total'] = df_filtered.groupby('City')['Total'].cumsum()
fig_area = px.area(
    df_filtered,
    x="Date",
    y="Cumulative Total",
    color="City",
    title="Área: Acúmulo de vendas no mês"
)
col2.plotly_chart(fig_area, use_container_width=True)

# Gráfico de Barra: Faturamento total diário (todas as cidades)
# Para cada dia = Soma(Vendas Yangon + Vendas Mandalay + Vendas Naypyitaw)
daily_total = df_filtered.groupby('Date')[['Total']].sum().reset_index()
fig_bar = px.bar(
    daily_total,
    x="Date",
    y="Total",
    title="Barra: Faturamento total diário (todas as cidades)"
)
col3.plotly_chart(fig_bar, use_container_width=True)

# --- 2. VISUALIZAÇÃO HIERÁRQUICA (TREEMAP) ---
# Nível 1 (Cidade): Soma de todas as vendas por cidade
# Nível 2 (Produto): Soma de vendas por categoria de produto dentro de cada cidade
st.header("2. Visualização Hierárquica (Treemap)")

fig_tree = px.treemap(
    df_filtered,
    path=['City', 'Product line'],
    values='Total',
    title='Treemap: Faturamento por Filial e Categoria'
)
st.plotly_chart(fig_tree, use_container_width=True)

# --- 3. VISUALIZAÇÃO GEOGRÁFICA ---
st.header("3. Visualização Geográfica")

# Coordenadas das cidades (adapte conforme seu dataset, se precisar)
#   Para cada cidade:
# - Latitude e Longitude (coordenadas geográficas)
# - Soma total de vendas = Soma de todas as transações da cidade
# - Tamanho do ponto = Proporcional ao valor total
city_coords = {
    "Yangon": {"lat": 16.8409, "lon": 96.1735},
    "Mandalay": {"lat": 21.9588, "lon": 96.0891},
    "Naypyitaw": {"lat": 19.7633, "lon": 96.0785},
}
df_filtered["lat"] = df_filtered["City"].map(lambda x: city_coords.get(x, {}).get("lat"))
df_filtered["lon"] = df_filtered["City"].map(lambda x: city_coords.get(x, {}).get("lon"))

fig_geo = px.scatter_geo(
    df_filtered,
    lat="lat",
    lon="lon",
    color="City",
    size="Total",
    hover_name="City",
    title="Distribuição Geográfica das Vendas (exemplo conceitual)"
)
st.plotly_chart(fig_geo, use_container_width=True)

# --- EXPLICAÇÃO FINAL ---
st.markdown("""
**Notas:**
- **Gráficos temporais:** mostram tendências e evolução do faturamento.
- **Treemap:** exibe a estrutura hierárquica das vendas por filial e categoria.
- **Mapa geográfico:** exemplifica a distribuição espacial das vendas (ajuste lat/lon se necessário).
""")
