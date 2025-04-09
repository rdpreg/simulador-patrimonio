
import streamlit as st
import matplotlib.pyplot as plt

def formata_reais(valor):
    return f"R$ {valor:,.2f}".replace(",", "v").replace(".", ",").replace("v", ".")


st.set_page_config(page_title="Projeção de Patrimônio (Acúmulo + Renda)", layout="centered")

st.markdown("""
<h1 style='margin-bottom: 0.0rem;'>Projeção de Patrimônio</h1>
<h4 style='margin-top: -0.5rem; margin-bottom: 0.3rem;'>Acúmulo + Renda</h4>
""", unsafe_allow_html=True)


st.markdown("### Fase 1: Acúmulo de Patrimônio")

# Inputs da fase de acúmulo
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
    

# Inputs da fase de renda
st.markdown("### Fase 2: Renda Passiva")

col1, col2 = st.columns(2)

with col1:
    anos_renda = st.slider("Prazo da Fase de Renda (anos)", 1, 50, 20)

with col2:
    taxa_renda_mensal = st.number_input("Taxa mensal na fase de renda (% ao mês)", min_value=0.0, max_value=5.0, value=0.5, step=0.01) / 100

# Título separado com menos espaçamento
#st.markdown("<h4 style='margin-bottom: 0.8rem;'>Simulações de Renda</h4>", unsafe_allow_html=True)

#st.markdown("<h4 style='margin-bottom: 0.3rem;'>Modelo de Renda</h4>", unsafe_allow_html=True)
#modelo = st.radio(label="", options=["Perpetuar o Patrimônio", "Consumir o Patrimônio todo"])


if st.button("Simular"):
    meses_acumulo = anos_acumulo * 12
    meses_renda = anos_renda * 12

    # Taxas equivalentes
    taxa_mensal = (1 + taxa_juros_anual / 100) ** (1/12) - 1
    taxa_renda_anual_equivalente = (1 + taxa_renda_mensal) ** 12 - 1

    # Fase 1 - Acúmulo
    valores = []
    for mes in range(meses_acumulo + 1):
        vf = aporte_inicial * (1 + taxa_mensal) ** mes + aporte_mensal * (((1 + taxa_mensal) ** mes - 1) / taxa_mensal)
        valores.append(vf)

    patrimonio_final = valores[-1]

    st.markdown("### Resultado da Fase de Acúmulo")
    st.write(f"- **Patrimônio final ao fim da fase de acúmulo:** {formata_reais(patrimonio_final)}")

    # Fase 2 - Simulação de Renda (2 modelos)

    # 1. Perpetuar o Patrimônio
    renda_perpetua = patrimonio_final * taxa_renda_mensal
    patrimonio_perpetuo = [patrimonio_final for _ in range(meses_renda + 1)]

    # 2. Consumir o Patrimônio todo
    if taxa_renda_mensal > 0:
        renda_consumo = patrimonio_final * (taxa_renda_mensal * (1 + taxa_renda_mensal) ** meses_renda) / ((1 + taxa_renda_mensal) ** meses_renda - 1)
    else:
        renda_consumo = patrimonio_final / meses_renda

    saldo = patrimonio_final
    patrimonio_consumo = []
    for _ in range(meses_renda + 1):
        patrimonio_consumo.append(saldo)
        saldo = saldo * (1 + taxa_renda_mensal) - renda_consumo

    # Exibir os dois resultados lado a lado
    st.markdown("### Resultado da Fase de Renda")
    col1, col2 = st.columns(2)

    with col1:
        st.subheader(" Perpetuar o Patrimônio")
        st.write(f"Renda mensal estimada: **{formata_reais(renda_perpetua)}**")
        st.write(f"Taxa anual: **{taxa_renda_anual_equivalente:.2%}**")

    with col2:
        st.subheader(" Consumir o Patrimônio todo")
        st.write(f"Renda mensal estimada: **{formata_reais(renda_consumo)}**")
        st.write(f"Prazo: **{anos_renda} anos**")
        st.write(f"Taxa anual: **{taxa_renda_anual_equivalente:.2%}**")

    # Gráfico das duas fases
    st.markdown("### Evolução do Patrimônio")
    fig, ax = plt.subplots(figsize=(10, 4))
    ax.plot(range(meses_acumulo + 1), valores, label="Acúmulo", color="green")
    ax.plot(range(meses_acumulo, meses_acumulo + meses_renda + 1), patrimonio_perpetuo, label="Renda (Perpétua)", linestyle="--", color="blue")
    ax.plot(range(meses_acumulo, meses_acumulo + meses_renda + 1), patrimonio_consumo, label="Renda (Consumo Total)", linestyle=":", color="red")
    ax.set_xlabel("Meses")
    ax.set_ylabel("Valor (R$)")
    ax.legend()
    ax.grid(True)
    st.pyplot(fig)
