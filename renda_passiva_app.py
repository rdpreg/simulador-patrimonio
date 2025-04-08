
import streamlit as st

# Configuração da página
st.set_page_config(page_title="Fase de Renda Passiva", layout="centered")

st.title("💸 Simulador de Renda Passiva")

st.markdown("""
Este simulador calcula quanto você pode retirar mensalmente do seu patrimônio acumulado
considerando dois cenários:

1. **Perpetuar o patrimônio:** viver de renda sem consumir o valor total investido.
2. **Gastar até zerar:** consumir todo o valor do patrimônio ao longo de um prazo determinado.
""")

# Entrada de dados
patrimonio_final = st.number_input("Patrimônio disponível (R$)", min_value=0.0, value=1000000.0, step=1000.0)
taxa_mensal = st.number_input("Taxa de rendimento mensal (%)", min_value=0.0, max_value=5.0, step=0.01, value=0.5) / 100
modelo = st.radio("Modelo de renda desejado", ["Perpetuar o Patrimônio", "Gastar até zerar"])

if modelo == "Gastar até zerar":
    prazo_meses = st.slider("Prazo para consumir o patrimônio (em anos)", 1, 50, 20) * 12

if st.button("Calcular Renda Mensal"):
    if modelo == "Perpetuar o Patrimônio":
        renda_mensal = patrimonio_final * taxa_mensal
    else:
        # Fórmula de saque mensal que zera o patrimônio no fim do prazo
        renda_mensal = patrimonio_final * (taxa_mensal * (1 + taxa_mensal) ** prazo_meses) / ((1 + taxa_mensal) ** prazo_meses - 1)

    st.success(f"📊 Sua renda mensal estimada seria: R$ {renda_mensal:,.2f}".replace(",", "v").replace(".", ",").replace("v", "."))
