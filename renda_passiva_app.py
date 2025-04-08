import streamlit as st
import matplotlib.pyplot as plt

# Configuração da página
st.set_page_config(page_title="Fase de Renda Passiva", layout="centered")

st.title(" Simulador de Renda Passiva")

st.markdown("""
Este simulador calcula quanto você pode retirar mensalmente do seu patrimônio acumulado
considerando dois cenários:

1. **Perpetuar o patrimônio**: viver de renda sem consumir o valor total investido.  
2. **Gastar até zerar**: consumir todo o valor do patrimônio ao longo de um prazo determinado.
""")

# Entrada de dados
patrimonio_final = st.number_input("Patrimônio disponível (R$)", min_value=0.0, value=1000000.0, step=1000.0)
taxa_mensal = st.number_input("Taxa de rendimento mensal (%)", min_value=0.0, max_value=5.0, step=0.01, value=0.5) / 100
prazo_anos = st.slider("Prazo para consumir o patrimônio (em anos)", 1, 50, 20)
prazo_meses = prazo_anos * 12

# Botão de cálculo
if st.button("Calcular Renda Mensal"):

    # Cenário 1: Perpetuar patrimônio
    renda_perpetua = patrimonio_final * taxa_mensal

    # Cenário 2: Renda até zerar (fórmula de saque mensal com prazo fixo)
    if taxa_mensal == 0:
        renda_prazo_fixo = patrimonio_final / prazo_meses  # evita divisão por zero
    else:
        renda_prazo_fixo = patrimonio_final * (taxa_mensal * (1 + taxa_mensal) ** prazo_meses) / ((1 + taxa_mensal) ** prazo_meses - 1)

    # Função de formatação
    def formata_reais(valor):
        return f"R$ {valor:,.2f}".replace(",", "v").replace(".", ",").replace("v", ".")

    # Mostrar os dois resultados lado a lado
    col1, col2 = st.columns(2)

    with col1:
        st.subheader(" Perpetuar o Patrimônio")
        st.write(f"Renda mensal vitalícia estimada:")
        st.success(formata_reais(renda_perpetua))

        # Gráfico
        fig1, ax1 = plt.subplots()
        ax1.plot(range(prazo_meses + 1), patrimonio_perpetuo, label="Patrimônio", color="green")
        ax1.set_title("Evolução do Patrimônio (Perpétuo)")
        ax1.set_xlabel("Meses")
        ax1.set_ylabel("Valor (R$)")
        ax1.grid(True)
        st.pyplot(fig1)

    with col2:
        st.subheader(" Gastar até zerar")
        st.write(f"Renda mensal por {prazo_anos} anos:")
        st.success(formata_reais(renda_prazo_fixo))

        # Gráfico
        fig2, ax2 = plt.subplots()
        ax2.plot(range(prazo_meses + 1), patrimonio_prazo, label="Patrimônio", color="orange")
        ax2.set_title("Evolução do Patrimônio (Prazo Fixo)")
        ax2.set_xlabel("Meses")
        ax2.set_ylabel("Valor (R$)")
        ax2.grid(True)
        st.pyplot(fig2)
