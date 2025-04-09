
import streamlit as st
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
from io import BytesIO
import base64


    
def formata_reais(valor):
    return f"R$ {valor:,.2f}".replace(",", "v").replace(".", ",").replace("v", ".")


st.set_page_config(page_title="Projeção de Patrimônio (Acúmulo + Renda)", layout="centered")

st.markdown("""
<h1 style='margin-bottom: 0.0rem;'>Projeção de Patrimônio</h1>
<h4 style='margin-top: -0.5rem; margin-bottom: 0.3rem;'>Acúmulo + Renda</h4>
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

# FASE 2 - Inputs
st.markdown("### Fase 2: Renda Passiva")

col5, col6 = st.columns(2)
with col5:
    anos_renda = st.slider("Prazo da Fase de Renda (anos)", 1, 50, 20)
with col6:
    taxa_renda_mensal = st.number_input("Taxa mensal na fase de renda (% ao mês)", min_value=0.0, max_value=5.0, value=0.5, step=0.01) / 100


# SIMULAR
if st.button("Simular"):
    meses_acumulo = anos_acumulo * 12
    meses_renda = anos_renda * 12

    taxa_mensal = (1 + taxa_juros_anual / 100) ** (1/12) - 1
    taxa_renda_anual_equivalente = (1 + taxa_renda_mensal) ** 12 - 1

    valores = []
    for mes in range(meses_acumulo + 1):
        vf = aporte_inicial * (1 + taxa_mensal) ** mes + aporte_mensal * (((1 + taxa_mensal) ** mes - 1) / taxa_mensal)
        valores.append(vf)

    patrimonio_final = valores[-1]
    renda_perpetua = patrimonio_final * taxa_renda_mensal

    if taxa_renda_mensal > 0:
        renda_consumo = patrimonio_final * (taxa_renda_mensal * (1 + taxa_renda_mensal) ** meses_renda) / ((1 + taxa_renda_mensal) ** meses_renda - 1)
    else:
        renda_consumo = patrimonio_final / meses_renda

    saldo = patrimonio_final
    patrimonio_consumo = []
    for _ in range(meses_renda + 1):
        patrimonio_consumo.append(saldo)
        saldo = saldo * (1 + taxa_renda_mensal) - renda_consumo

    patrimonio_perpetuo = [patrimonio_final for _ in range(meses_renda + 1)]

    st.session_state["simulacao"] = {
        "valores": valores,
        "patrimonio_final": patrimonio_final,
        "renda_perpetua": renda_perpetua,
        "renda_consumo": renda_consumo,
        "patrimonio_consumo": patrimonio_consumo,
        "patrimonio_perpetuo": patrimonio_perpetuo,
        "anos_acumulo": [m / 12 for m in range(meses_acumulo + 1)],
        "anos_renda_offset": [m / 12 + anos_acumulo for m in range(meses_renda + 1)],
        "taxa_renda_anual_equivalente": taxa_renda_anual_equivalente,
        "anos_renda": anos_renda
    }

# MOSTRAR RESULTADOS
if "simulacao" in st.session_state:
    sim = st.session_state["simulacao"]

    st.markdown("### Resultado da Fase de Acúmulo")

    # Calcular valores
    patrimonio_final = sim['patrimonio_final']
    meses_aporte = anos_acumulo * 12
    total_investido = aporte_inicial + (aporte_mensal * meses_aporte)
    total_rendimentos = patrimonio_final - total_investido

    # Exibir resultados
    st.write(f"- **Patrimônio final ao fim da fase de acúmulo:** {formata_reais(patrimonio_final)}")
    st.write(f"- Aporte inicial: {formata_reais(aporte_inicial)}")
    st.write(f"- Total investido (incluindo aportes mensais): {formata_reais(total_investido)}")
    st.write(f"- Total de rendimentos acumulados: {formata_reais(total_rendimentos)}")
    )

    st.markdown("### Resultado da Fase de Renda")
    col1, col2 = st.columns(2)
    with col1:
        st.subheader(" Perpetuar o Patrimônio")
        st.write(f"Renda mensal estimada: **{formata_reais(sim['renda_perpetua'])}**")
        st.write(f"Taxa anual: **{sim['taxa_renda_anual_equivalente']:.2%}**")
    with col2:
        st.subheader(" Consumo Total")
        st.write(f"Renda mensal estimada: **{formata_reais(sim['renda_consumo'])}**")
        st.write(f"Prazo: **{sim['anos_renda']} anos**")

    st.markdown("### Evolução do Patrimônio")
    fig, ax = plt.subplots(figsize=(10, 4))
    ax.plot(sim['anos_acumulo'], sim['valores'], label="Acúmulo", color="green")
    ax.plot(sim['anos_renda_offset'], sim['patrimonio_perpetuo'], label="Renda (Perpétua)", linestyle="--", color="blue")
    ax.plot(sim['anos_renda_offset'], sim['patrimonio_consumo'], label="Renda (Consumo Total)", linestyle=":", color="red")
    ax.set_xlabel("Anos")
    ax.set_ylabel("Valor (R$)")
    ax.yaxis.set_major_formatter(mtick.FuncFormatter(lambda x, _: f"R$ {x:,.2f}".replace(",", "v").replace(".", ",").replace("v", ".")))
    ax.legend()
    ax.grid(True)
    st.pyplot(fig)

    
