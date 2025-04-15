
import streamlit as st
import plotly.graph_objects as go
import pandas as pd

def formata_reais(valor):
    return f"R$ {valor:,.2f}".replace(",", "v").replace(".", ",").replace("v", ".")

st.set_page_config(page_title="Simulador de Patrimônio (Fase 1 - Acúmulo)", layout="centered")
st.image("Convexa-logo.png", width=180)
st.markdown("<h1 style='margin-bottom: 0.0rem;'>Simulador de Patrimônio</h1>", unsafe_allow_html=True)
st.markdown("### Fase 1: Acúmulo de Patrimônio")

# Inputs
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

    #Relatório da projeção
    st.markdown("### Resultado da Fase de Acúmulo")
    st.write(f"- **Patrimônio final ao fim do período:** {formata_reais(patrimonio_final)}")
    st.write(f"- Aporte inicial: {formata_reais(aporte_inicial)}")
    st.write(f"- Total aportado ao longo do período: {formata_reais(total_aportes)}")
    st.write(f"- Total de rendimentos acumulados: {formata_reais(rendimento_total)}")


    anos = [m / 12 for m in range(meses_acumulo + 1)]
    anos_formatados = [f"{a:.1f}".replace(".", ",") for a in anos]
    valores_formatados = [formata_reais(v) for v in valores]
    
    if meta_valor > 0:
        st.write(f"- **Meta definida:** {formata_reais(meta_valor)}")
        ano_atingido = None
        for i, v in enumerate(valores):
            if v >= meta_valor:
                meses_atingido = i
                break

        if meses_atingido is not None and meses_atingido <= meses_acumulo:
            anos_cheios = meses_atingido // 12
            meses_restantes = meses_atingido % 12
            texto_meta = f"🎯 Você alcançará seu objetivo em **{anos_cheios} anos"
            if meses_restantes > 0:
                texto_meta += f" e {meses_restantes} meses"
            texto_meta += "**."

            st.success(texto_meta)
        else:
            st.warning("⚠️ Com os parâmetros atuais, a meta **não será atingida** no período simulado.")

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

    # Gráfico de barras stacked
    anos_cheios = [int(a) for a in anos if a.is_integer()]
    anos_filtrados = sorted(list(set(anos_cheios)))
    valores_ano = [valores[int(a * 12)] for a in anos_filtrados]
    aporte_ano = [aporte_inicial + aporte_mensal * int(a * 12) for a in anos_filtrados]
    rendimento_ano = [v - a for v, a in zip(valores_ano, aporte_ano)]

    df_stack = pd.DataFrame({
        "Ano": anos_filtrados,
        "Aportes": aporte_ano,
        "Rendimentos": rendimento_ano
    })

    fig_bar = go.Figure()
    fig_bar.add_trace(go.Bar(x=df_stack["Ano"], y=df_stack["Aportes"], name="Aportes", marker_color="orange"))
    fig_bar.add_trace(go.Bar(x=df_stack["Ano"], y=df_stack["Rendimentos"], name="Rendimentos", marker_color="green"))
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
    fig_bar.add_shape(
        type="line",
        xref="paper", yref="y",
        x0=0, x1=1,
        y0=meta_valor, y1=meta_valor,
        line=dict(color="red", width=2, dash="dash")
    )
    fig_bar.add_annotation(
        xref="paper", yref="y",
        x=1, y=meta_valor,
        text=f"Meta: {formata_reais(meta_valor)}",
        showarrow=False,
        font=dict(color="red", size=12),
        xanchor="left",
        yanchor="bottom"
    )
    st.plotly_chart(fig_bar, use_container_width=True)

    # Salvar resultado para próxima fase
    st.session_state["patrimonio_final"] = patrimonio_final



# =====================
# FASE 2 - RENDA PASSIVA
# =====================
st.markdown("### Fase 2: Renda Passiva")

if "patrimonio_final" in st.session_state:
    patrimonio_base = st.session_state["patrimonio_final"]

    col1, col2 = st.columns(2)
    with col1:
        anos_renda = st.slider("Prazo da Fase de Renda (anos)", 1, 50, 20)
    with col2:
        taxa_renda_mensal = st.number_input(
            "Taxa de rentabilidade mensal (% ao mês)",
            min_value=0.0, max_value=5.0, value=0.5, step=0.01
        ) / 100

    meses_renda = anos_renda * 12
    taxa_anual_equivalente = (1 + taxa_renda_mensal) ** 12 - 1

    # Modelo 1 - Renda Perpétua
    renda_perpetua = patrimonio_base * taxa_renda_mensal

    # Modelo 2 - Consumo Total
    if taxa_renda_mensal > 0:
        renda_consumo = patrimonio_base * (
            taxa_renda_mensal * (1 + taxa_renda_mensal) ** meses_renda
        ) / ((1 + taxa_renda_mensal) ** meses_renda - 1)
    else:
        renda_consumo = patrimonio_base / meses_renda

    saldo = patrimonio_base
    patrimonio_consumo = []
    for _ in range(meses_renda + 1):
        patrimonio_consumo.append(saldo)
        saldo = saldo * (1 + taxa_renda_mensal) - renda_consumo

    patrimonio_perpetuo = [patrimonio_base for _ in range(meses_renda + 1)]

    st.markdown("### Resultado da Fase de Renda")
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Perpetuar o Patrimônio")
        st.write(f"Renda mensal estimada: **{formata_reais(renda_perpetua)}**")
        st.write(f"Taxa anual: **{taxa_anual_equivalente:.2%}**")
    with col2:
        st.subheader("Consumo Total")
        st.write(f"Renda mensal estimada: **{formata_reais(renda_consumo)}**")
        st.write(f"Prazo: **{anos_renda} anos**")

    # Gráfico
    anos_renda = [m / 12 for m in range(meses_renda + 1)]
    anos_renda_offset = [m / 12 + anos_acumulo for m in range(meses_renda + 1)]

    fig_renda = go.Figure()
    fig_renda.add_trace(go.Scatter(x=anos, y=valores, name="Acúmulo", line=dict(color="green")))
    fig_renda.add_trace(go.Scatter(x=anos_renda_offset, y=patrimonio_perpetuo, name="Renda (Perpétua)", line=dict(color="blue", dash="dash")))
    fig_renda.add_trace(go.Scatter(x=anos_renda_offset, y=patrimonio_consumo, name="Renda (Consumo Total)", line=dict(color="red", dash="dot")))

    fig_renda.update_layout(
        title="Evolução do Patrimônio - Fase 1 + Fase 2",
        xaxis_title="Ano",
        yaxis_title="Valor (R$)",
        hovermode="x unified",
        font=dict(family="Arial", size=14),
        yaxis_tickprefix="R$ ",
        yaxis_tickformat=",.2f",
        margin=dict(t=50, l=50, r=30, b=50)
    )

    st.plotly_chart(fig_renda, use_container_width=True)

else:
    st.info("⚠️ Simule a Fase 1 primeiro para liberar a Fase 2.")
