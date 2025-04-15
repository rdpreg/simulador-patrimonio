
import streamlit as st
import plotly.graph_objects as go
import pandas as pd

def formata_reais(valor):
    return f"R$ {valor:,.2f}".replace(",", "v").replace(".", ",").replace("v", ".")

st.set_page_config(page_title="Simulador de Patrimônio (Fase 1 - Acúmulo)", layout="centered")
st.image("Convexa-logo.png", width=180)
st.markdown("<h1 style='margin-bottom: 0.0rem;'>Simulador de Patrimônio</h1>", unsafe_allow_html=True)
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

# Input da meta ANTES do botão
meta_valor = st.number_input(
    "Defina sua meta de patrimônio (R$)",
    min_value=0.0,
    value=1000000.0,
    step=50000.0,
    format="%.2f"
)

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

    anos = [m / 12 for m in range(meses_acumulo + 1)]
    anos_formatados = [f"{a:.1f}".replace(".", ",") for a in anos]
    valores_formatados = [formata_reais(v) for v in valores]

    df = pd.DataFrame({
        "Ano": anos,
        "Ano BR": anos_formatados,
        "Patrimônio": valores,
        "Patrimônio BR": valores_formatados
    })

    tick_vals = list(range(0, int(max(valores) * 1.1), int(max(valores) / 6)))
    tick_text = [formata_reais(v) for v in tick_vals]

    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=df["Ano"],
        y=df["Patrimônio"],
        mode="lines",
        line=dict(color="green", width=2),
        customdata=df[["Ano BR", "Patrimônio BR"]],
        hovertemplate="<b>Ano:</b> %{customdata[0]}<br><b>Patrimônio:</b> %{customdata[1]}<extra></extra>",
        showlegend=False
    ))

    fig.add_shape(
        type="line",
        x0=min(df["Ano"]),
        x1=max(df["Ano"]),
        y0=meta_valor,
        y1=meta_valor,
        line=dict(color="red", width=2, dash="dash")
    )

    fig.add_annotation(
        x=max(df["Ano"]),
        y=meta_valor,
        text=f"Meta: {formata_reais(meta_valor)}",
        showarrow=False,
        font=dict(color="red", size=12),
        xanchor="left",
        yanchor="bottom"
    )

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
