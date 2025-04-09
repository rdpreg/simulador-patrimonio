
import streamlit as st
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick

#Geração do relatório
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from io import BytesIO
import base64


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
        st.subheader(" Consumo Total")
        st.write(f"Renda mensal estimada: **{formata_reais(renda_consumo)}**")
        st.write(f"Prazo: **{anos_renda} anos**")
        

    # Gráfico das duas fases
    st.markdown("### Evolução do Patrimônio")
    # Eixo X em anos
    anos_acumulo = [m / 12 for m in range(meses_acumulo + 1)]
    anos_renda = [m / 12 for m in range(meses_renda + 1)]
    anos_renda_offset = [m / 12 + anos_acumulo[-1] for m in range(meses_renda + 1)]

    fig, ax = plt.subplots(figsize=(10, 4))
    ax.plot(anos_acumulo, valores, label="Acúmulo", color="green")
    ax.plot(anos_renda_offset, patrimonio_perpetuo, label="Renda (Perpétua)", linestyle="--", color="blue")
    ax.plot(anos_renda_offset, patrimonio_consumo, label="Renda (Consumo Total)", linestyle=":", color="red")

    ax.set_xlabel("Anos")
    ax.set_ylabel("Valor (R$)")
    ax.yaxis.set_major_formatter(mtick.FuncFormatter(lambda x, _: f"R$ {x:,.2f}".replace(",", "v").replace(".", ",").replace("v", ".")))
    ax.legend()
    ax.grid(True)
    st.pyplot(fig)

    

    # Botão para gerar PDF
    if st.button("📄 Gerar PDF do Relatório"):
    # Salvar gráfico
    fig.savefig("grafico_simulador.png")

    # Criar PDF
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4

    c.setFont("Helvetica-Bold", 16)
    c.drawString(50, height - 50, "Relatório de Simulação de Patrimônio")

    c.setFont("Helvetica", 12)
    y = height - 90
    c.drawString(50, y, f"Patrimônio Final Acumulado: {formata_reais(patrimonio_final)}")
    y -= 20
    c.drawString(50, y, f"Renda mensal (Perpétua): {formata_reais(renda_perpetua)}")
    y -= 20
    c.drawString(50, y, f"Renda mensal (Consumir até zerar): {formata_reais(renda_consumo)}")
    y -= 20
    c.drawString(50, y, f"Prazo de Renda: {anos_renda} anos")
    y -= 20
    c.drawString(50, y, f"Taxa anual da fase de renda: {taxa_renda_anual_equivalente:.2%}")

    # Inserir gráfico
    if os.path.exists("grafico_simulador.png"):
        c.drawImage("grafico_simulador.png", 50, y - 280, width=500, preserveAspectRatio=True)

    c.save()

    # Download do PDF
    buffer.seek(0)
    b64_pdf = base64.b64encode(buffer.read()).decode('utf-8')
    href = f'<a href="data:application/octet-stream;base64,{b64_pdf}" download="relatorio_simulador.pdf">📥 Clique aqui para baixar o PDF</a>'
    st.markdown(href, unsafe_allow_html=True)

