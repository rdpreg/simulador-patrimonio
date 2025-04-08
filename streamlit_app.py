
import streamlit as st
import matplotlib.pyplot as plt

st.set_page_config(page_title="Projeção de Patrimônio", layout="centered")

# Cabeçalho com logo e título
cols = st.columns([1, 4])
cols[0].image("https://drive.google.com/uc?id=1rlJl0tLEFCSgO3HJBkDq_ZmIRszjVOEw", width=100)  # Troque o nome se for diferente
cols[1].markdown("## Projção de Patrimônio")

# --- Entradas do usuário ---
patrimonio_inicial = st.number_input("Patrimônio Inicial (R$)", min_value=0.0, value=50000.0, step=1000.0)
aporte_mensal = st.number_input("Aporte Mensal (R$)", min_value=0.0, value=2000.0, step=100.0)
taxa_juros_anual = st.slider("Juros (% a.a.)", min_value=0.0, max_value=20.0, step=0.1, value=10.0)
anos = st.slider("Prazo (anos)", min_value=1, max_value=50, value=20)

# --- Botão de simulação ---
if st.button("Simular"):
    meses = anos * 12
    taxa_mensal = taxa_juros_anual / 100 / 12
    valores = []
    aportes = []

    for mes in range(meses + 1):
        vf = patrimonio_inicial * (1 + taxa_mensal) ** mes + \
            aporte_mensal * (((1 + taxa_mensal) ** mes - 1) / taxa_mensal)
        aporte_total = patrimonio_inicial + aporte_mensal * mes
        valores.append(vf)
        aportes.append(aporte_total)

    juros = valores[-1] - aportes[-1]

    st.subheader("Resultado Final")
    st.write(f"**Total Investido:** R$ {aportes[-1]:,.2f}")
    st.write(f"**Patrimônio Acumulado:** R$ {valores[-1]:,.2f}")
    st.write(f"**Juros Rendidos:** R$ {juros:,.2f}")

    # Gráfico
    fig, ax = plt.subplots(figsize=(10, 4))
    ax.plot(range(meses + 1), valores, label="Patrimônio Acumulado", color='green')
    ax.plot(range(meses + 1), aportes, label="Total Investido", linestyle='--', color='gray')
    ax.set_xlabel("Meses")
    ax.set_ylabel("Valor (R$)")
    ax.set_title("Evolução do Patrimônio")
    ax.legend()
    ax.grid(True)
    st.pyplot(fig)
