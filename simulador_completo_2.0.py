
import streamlit as st
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
from io import BytesIO
import base64

def formata_reais(valor):
    return f"R$ {valor:,.2f}".replace(",", "v").replace(".", ",").replace("v", ".")

st.set_page_config(page_title="Simulador de Patrimônio (Fase 1 - Acúmulo)", layout="centered")

st.image("Convexa-logo.png", width=180)

st.markdown("""
<h1 style='margin-bottom: 0.0rem;'>Simulador de Patrimônio</h1>
""", unsafe_allow_html=True)

# FASE 1 - Inputs
st.markdown("### Fase 1: Acúmulo de Patrimônio")

col1, col2 = st.columns(2)
with col1:
    aporte_inicial = st.number_input("Aporte Inicial (R$)", min_value=0.0, value=50000.0, step=100.0, format="%.2f")
with col2:
    aporte_mensal = st.number_input("Aporte Mensal (R$)", min_value=0.0, value=2000.0, step=100.0, format="%.2f")

col3, col4 = st.columns(2)
with col3:
    taxa_juros_anual = st.number_input("Taxa de Juros Anual (%)", min_value=0.0, max_value=30.0, value=10.0, step=0.1)
with col4:
    anos_acumulo = st.slider("Prazo da Fase de Acúmulo (anos)", 1, 50, 20)

# SIMULAR ACÚMULO
if st.button("Simular Acúmulo"):
    meses_acumulo = anos_acumulo * 12
    taxa_mensal = (1 + taxa_juros_anual / 100) ** (1 / 12) - 1

    valores = []
    for mes in range(meses_acumulo + 1):
        vf = aporte_inicial * (1 + taxa_mensal) ** mes + aporte_mensal * (((1 + taxa_mensal) ** mes - 1) / taxa_mensal)
        valores.append(vf)

    patrimonio_final = valores[-1]
    total_aportes = aporte_inicial + (aporte_mensal * meses_acumulo)
    rendimento_total = patrimonio_final - total_aportes

    st.markdown("### Resultado da Fase de Acúmulo")
    st.write(f"- **Patrimônio final ao fim do período:** {formata_reais(patrimonio_final)}")
    st.write(f"- Aporte inicial: {formata_reais(aporte_inicial)}")
    st.write(f"- Total aportado ao longo do período: {formata_reais(total_aportes)}")
    st.write(f"- Total de rendimentos acumulados: {formata_reais(rendimento_total)}")

    #Gráficos

    #Gráfico de linha - acúmulo de patrimônio
    anos = [m / 12 for m in range(meses_acumulo + 1)]
    anos_formatados = [f"{a:.1f}".replace(".", ",") for a in anos]
    valores_formatados = [f"R$ {v:,.2f}".replace(",", "v").replace(".", ",").replace("v", ".") for v in valores]

    df = pd.DataFrame({
        "Ano": anos,
        "Ano BR": anos_formatados,
        "Patrimônio": valores,
        "Patrimônio BR": valores_formatados
    })

    # Formatando eixo Y manualmente
    tick_vals = list(range(0, int(max(valores) * 1.1), int(max(valores) / 6)))
    tick_text = [f"R$ {val:,.2f}".replace(",", "v").replace(".", ",").replace("v", ".") for val in tick_vals]

    # Criar gráfico com go.Figure
    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=df["Ano"],
        y=df["Patrimônio"],
        mode="lines",  # apenas linha
        line=dict(color="green", width=2),  # controle total do traço
        hovertemplate="<b>Ano:</b> %{customdata[0]}<br><b>Patrimônio:</b> %{customdata[1]}<extra></extra>",
        customdata=df[["Ano BR", "Patrimônio BR"]],
        showlegend=False,
        name=""
    ))

    fig.update_layout(
        title="Evolução do Patrimônio Acumulado",
        hovermode="x unified",
        font=dict(family="Arial", size=14),
        title_font_size=18,
        xaxis_title="Ano",
        yaxis=dict(
            title="Valor acumulado",
            tickvals=tick_vals,
            ticktext=tick_text
        ),
        margin=dict(t=50, l=50, r=30, b=50)
    )

    st.plotly_chart(fig, use_container_width=True)

    import plotly.graph_objects as go

    #Gráfico de barras - aporte x rendimentos ano a ano
    # Dados por ano (filtrando apenas 1 valor por ano)
    anos_cheios = [int(a) for a in anos if a.is_integer()]
    anos_filtrados = sorted(list(set(anos_cheios)))
    valores_ano = [valores[int(a * 12)] for a in anos_filtrados]

    # Cálculo de aportes acumulados por ano
    aporte_ano = [aporte_inicial + aporte_mensal * int(a * 12) for a in anos_filtrados]
    rendimento_ano = [v - a for v, a in zip(valores_ano, aporte_ano)]

    df_stack = pd.DataFrame({
        "Ano": anos_filtrados,
        "Aportes": aporte_ano,
        "Rendimentos": rendimento_ano
    })

    fig_bar = go.Figure()

    fig_bar.add_trace(go.Bar(
        x=df_stack["Ano"],
        y=df_stack["Aportes"],
        name="Aportes",
        marker_color="orange",
        hovertemplate="Ano: %{x}<br>Aportes: R$ %{y:,.2f}<extra></extra>"
    ))

    fig_bar.add_trace(go.Bar(
        x=df_stack["Ano"],
        y=df_stack["Rendimentos"],
        name="Rendimentos",
        marker_color="green",
        hovertemplate="Ano: %{x}<br>Rendimentos: R$ %{y:,.2f}<extra></extra>"
    ))

    fig_bar.update_layout(
        barmode="stack",
        title="Composição do Patrimônio Acumulado por Ano",
        xaxis_title="Ano",
        yaxis_title="Valor (R$)",
        hovermode="x unified",
        font=dict(family="Arial", size=14),
        yaxis_tickprefix="R$ ",
        yaxis_tickformat=",.2f",
        margin=dict(t=50, l=50, r=30, b=50)
    )

    st.plotly_chart(fig_bar, use_container_width=True)



    # Salvar resultado para próxima fase (opcional)
    st.session_state["patrimonio_final"] = patrimonio_final
