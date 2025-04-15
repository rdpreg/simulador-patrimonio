
import streamlit as st
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
from io import BytesIO
import base64

def formata_reais(valor):
    return f"R$ {valor:,.2f}".replace(",", "v").replace(".", ",").replace("v", ".")

st.set_page_config(page_title="Simulador de Patrimônio (Fase 1 - Acúmulo)", layout="centered")

st.image("Convexa-logo.png", width=180)

st.markdown("""
<h1 style='margin-bottom: 0.0rem;'>Simulador de Patrimônio</h1>
<h4 style='margin-top: -0.5rem; margin-bottom: 0.3rem;'>Fase 1: Acúmulo</h4>
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

    anos = [m / 12 for m in range(meses_acumulo + 1)]
    fig, ax = plt.subplots(figsize=(10, 4))
    ax.plot(anos, valores, label="Evolução do Patrimônio", color="green")
    ax.set_xlabel("Anos")
    ax.set_ylabel("Valor (R$)")
    ax.yaxis.set_major_formatter(mtick.FuncFormatter(lambda x, _: f"R$ {x:,.2f}".replace(",", "v").replace(".", ",").replace("v", ".")))
    ax.grid(True)
    st.pyplot(fig)

    # Salvar resultado para próxima fase (opcional)
    st.session_state["patrimonio_final"] = patrimonio_final
