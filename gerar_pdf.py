
import streamlit as st
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
from io import BytesIO
from weasyprint import HTML
import base64


def formata_reais(valor):
    return f"R$ {valor:,.2f}".replace(",", "v").replace(".", ",").replace("v", ",")


def gerar_pdf(sim, aporte_inicial, aporte_mensal, taxa_juros_anual, anos_acumulo):
    # Gerar gráfico
    fig, ax = plt.subplots(figsize=(10, 4))
    ax.plot(sim['anos_acumulo'], sim['valores'], label="Acúmulo", color="green")
    ax.plot(sim['anos_renda_offset'], sim['patrimonio_perpetuo'], label="Renda (Perpétua)", linestyle="--", color="blue")
    ax.plot(sim['anos_renda_offset'], sim['patrimonio_consumo'], label="Renda (Consumo Total)", linestyle=":", color="red")
    ax.set_xlabel("Anos")
    ax.set_ylabel("Valor (R$)")
    ax.yaxis.set_major_formatter(mtick.FuncFormatter(lambda x, _: f"R$ {x:,.2f}".replace(",", "v").replace(".", ",").replace("v", ",")))
    ax.legend()
    ax.grid(True)

    buffer_grafico = BytesIO()
    fig.savefig(buffer_grafico, format="png", bbox_inches='tight')
    buffer_grafico.seek(0)
    imagem_base64 = base64.b64encode(buffer_grafico.read()).decode("utf-8")

    # HTML estilizado
    html = f'''
    <html>
    <head>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 40px; }}
        h2 {{ color: #222; }}
        .coluna {{ width: 48%; display: inline-block; vertical-align: top; }}
        img {{ width: 100%; margin-top: 20px; }}
    </style>
    </head>
    <body>
        <h2>Resultado da Fase de Acúmulo</h2>
        <p><strong>Patrimônio final ao fim da fase de acúmulo:</strong> {formata_reais(sim['patrimonio_final'])}</p>

        <h2>Resultado da Fase de Renda</h2>
        <div class="coluna">
            <h3>Perpetuar o Patrimônio</h3>
            <p><strong>Renda mensal estimada:</strong> {formata_reais(sim['renda_perpetua'])}</p>
            <p><strong>Taxa anual:</strong> {sim['taxa_renda_anual_equivalente']:.2%}</p>
        </div>
        <div class="coluna">
            <h3>Consumo Total</h3>
            <p><strong>Renda mensal estimada:</strong> {formata_reais(sim['renda_consumo'])}</p>
            <p><strong>Prazo:</strong> {sim['anos_renda']} anos</p>
        </div>

        <h2>Evolução do Patrimônio</h2>
        <img src="data:image/png;base64,{imagem_base64}" />
    </body>
    </html>
    '''

    buffer_pdf = BytesIO()
    HTML(string=html).write_pdf(buffer_pdf)
    buffer_pdf.seek(0)
    return buffer_pdf
