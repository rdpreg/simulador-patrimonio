
import streamlit as st
import matplotlib.pyplot as plt

st.set_page_config(page_title="Projeção de Patrimônio (Acúmulo + Renda)", layout="centered")

st.markdown("""
<h1 style='margin-bottom: 0.5rem;'>Projeção de Patrimônio</h1>
<h4 style='margin-top: 0.2rem; margin-bottom: 0.3rem;'>Acúmulo + Renda</h4>
""", unsafe_allow_html=True)

#st.title("Projeção de Patrimônio")
#st.markdown("<h4 style='margin-bottom: 0.3rem;'>Acúmulo + Renda</h4>", unsafe_allow_html=True)


#st.markdown("### Acúmulo + Renda")

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
st.markdown("<h4 style='margin-bottom: 0.3rem;'>Modelo de Renda</h4>", unsafe_allow_html=True)
modelo = st.radio(label="", options=["Perpetuar o Patrimônio", "Consumir o Patrimônio todo"])


# Taxa de rendimento exclusiva para a fase de renda
#taxa_renda_mensal = st.number_input("Taxa mensal na fase de renda (% ao mês)", min_value=0.0, max_value=5.0, value=0.5, step=0.01) / 100


if st.button("Simular"):
    meses_acumulo = anos_acumulo * 12
    meses_renda = anos_renda * 12
    taxa_mensal = (1 + taxa_juros_anual / 100) ** (1/12) - 1
    taxa_renda_anual_equivalente = (1 + taxa_renda_mensal) ** 12 - 1
    


    # Fase 1 - Acúmulo
    valores = []
    for mes in range(meses_acumulo + 1):
        vf = aporte_inicial * (1 + taxa_mensal) ** mes + aporte_mensal * (((1 + taxa_mensal) ** mes - 1) / taxa_mensal)
        valores.append(vf)

    patrimonio_final = valores[-1]

    # Fase 2 - Renda
    patrimonio_renda = []
    if modelo == "Perpetuar o Patrimônio":
        renda_mensal = patrimonio_final * taxa_renda_mensal
        patrimonio_renda = [patrimonio_final for _ in range(meses_renda + 1)]
    else:
        if taxa_mensal == 0:
            renda_mensal = patrimonio_final / meses_renda
            patrimonio_renda = [patrimonio_final - renda_mensal * m for m in range(meses_renda + 1)]
        else:
            renda_mensal = patrimonio_final * (taxa_mensal * (1 + taxa_mensal) ** meses_renda) / ((1 + taxa_mensal) ** meses_renda - 1)
            saldo = patrimonio_final
            for _ in range(meses_renda + 1):
                patrimonio_renda.append(saldo)
                saldo = saldo * (1 + taxa_mensal) - renda_mensal

    # Concatenar fases para o gráfico completo
    patrimonio_total = valores + patrimonio_renda[1:]  # remove duplicação no ponto de transição

    # Função de formatação
    def formata_reais(valor):
        return f"R$ {valor:,.2f}".replace(",", "v").replace(".", ",").replace("v", ".")

    # Resultados
    st.markdown("### Resultado da Simulação")
    st.write(f"**Patrimônio ao final da fase de acúmulo:** {formata_reais(patrimonio_final)}")
    st.write(f"**Renda mensal estimada na fase de renda:** {formata_reais(renda_mensal)}")
    st.write(f"**Taxa anual equivalente da fase de renda:** {taxa_renda_anual_equivalente * 100:.2f}%")

    # Gráfico final
    fig, ax = plt.subplots(figsize=(10, 4))
    ax.plot(range(len(patrimonio_total)), patrimonio_total, label="Evolução do Patrimônio", color="green")
    ax.axvline(x=meses_acumulo, color='gray', linestyle='--', label="Início da Renda")
    ax.set_xlabel("Meses")
    ax.set_ylabel("Valor (R$)")
    ax.set_title("Simulação Completa: Acúmulo + Renda")
    ax.legend()
    ax.grid(True)
    st.pyplot(fig)
