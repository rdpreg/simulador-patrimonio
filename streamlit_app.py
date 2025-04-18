
import streamlit as st
import matplotlib.pyplot as plt

def formata_reais(valor):
        return f"R$ {valor:,.2f}".replace(",", "v").replace(".", ",").replace("v", ".")


st.set_page_config(page_title="Projeção de Patrimônio", layout="centered")

# Cabeçalho com logo e título
cols = st.columns([1, 4])
cols[0].image("https://drive.google.com/uc?id=1rlJl0tLEFCSgO3HJBkDq_ZmIRszjVOEw", width=100)  # Troque o nome se for diferente
cols[1].markdown("## Projeção de Patrimônio")

# --- Entradas do usuário ---
def formata_reais(valor):
    return f"R$ {valor:,.2f}".replace(",", "v").replace(".", ",").replace("v", ".")
patrimonio_inicial = st.number_input("Patrimônio Inicial (R$)", min_value=0.0, value=50000.0, step=100.0)
st.caption(f"Valor digitado: {formata_reais(patrimonio_inicial)}")
aporte_mensal = st.number_input("Aporte Mensal (R$)", min_value=0.0, value=2000.0, step=100.0)
st.caption(f"Valor digitado: {formata_reais(aporte_mensal)}")
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
        aporte_inicial = patrimonio_inicial
        aporte_recorrente = aporte_mensal * meses
        aporte_total = aporte_inicial + aporte_recorrente
        aporte_total_mes = patrimonio_inicial + aporte_mensal * mes
        valores.append(vf)
        aportes.append(aporte_total_mes)
        
    #AQUI: separação dos aportes
    aporte_inicial = patrimonio_inicial
    aporte_recorrente = aporte_mensal * meses
    aporte_total_final = aporte_inicial + aporte_recorrente    
    juros = valores[-1] - aporte_total_final

    #Exibição
    st.subheader("Resultado Final")
    st.write(f"**Aporte Inicial:** {formata_reais(aporte_inicial)}")
    st.write(f"**Aportes Mensais:** {formata_reais(aporte_recorrente)}")
    st.write(f"**Total Investido:** {formata_reais(aporte_total)}")
    st.write(f"**Patrimônio Acumulado:** {formata_reais(valores[-1])}")
    st.write(f"**Juros Rendidos:** {formata_reais(valores[-1] - aporte_total)}")


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
