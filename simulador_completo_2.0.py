
import streamlit as st
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
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

    #gráfico
    anos = [m / 12 for m in range(meses_acumulo + 1)]

    # Formatar ano e patrimônio para estilo brasileiro
    anos_formatados = [f"{a:.1f}".replace(".", ",") for a in anos]
    valores_formatados = [f"R$ {v:,.2f}".replace(",", "v").replace(".", ",").replace("v", ".") for v in valores]

    df = pd.DataFrame({
        "Ano": anos,
        "Ano BR": anos_formatados,
        "Patrimônio": valores,
        "Patrimônio BR": valores_formatados
    })

    # Eixo Y personalizado
    tick_vals = list(range(0, int(max(valores) * 1.1), int(max(valores) / 6)))
    tick_text = [f"R$ {val:,.2f}".replace(",", "v").replace(".", ",").replace("v", ".") for val in tick_vals]

    # Criar gráfico
    fig = px.line(
        df,
        x="Ano",
        y="Patrimônio",
        title="Evolução do Patrimônio Acumulado",
        markers=True
    )

    fig.update_traces(
        mode="lines",  # 👈 isso força a exibição do traço
        line=dict(color="green", width=1),
        customdata=df[["Ano BR", "Patrimônio BR"]],
        hovertemplate="<b>Ano:</b> %{customdata[0]}<br><b>Patrimônio:</b> %{customdata[1]}<extra></extra>"
    )

    fig.update_layout(
        hovermode="x unified",
        title_font_size=18,
        font=dict(family="Arial", size=14),
        yaxis=dict(
            title="Valor acumulado",
            tickvals=tick_vals,
            ticktext=tick_text
        ),
        xaxis_title="Ano",
        margin=dict(t=50, l=50, r=30, b=50)
    )

    st.plotly_chart(fig, use_container_width=True)


    # Salvar resultado para próxima fase (opcional)
    st.session_state["patrimonio_final"] = patrimonio_final
