
# Aqui entra todo o código do simulador completo já com Fase 1 e Fase 2.
# Para simplificar aqui, vamos apenas declarar o marcador final com o botão PDF,
# considerando que você já tem o restante do simulador funcionando.

# ==========================
# Botão para gerar PDF
# ==========================
import base64
from io import BytesIO
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.utils import ImageReader

if "patrimonio_final" in st.session_state and "valores" in st.session_state:
    if st.button("📄 Gerar PDF do Relatório"):
        buffer_linha = BytesIO()
        fig_renda.write_image(buffer_linha, format="png")
        buffer_linha.seek(0)

        buffer_barra = BytesIO()
        fig_bar.write_image(buffer_barra, format="png")
        buffer_barra.seek(0)

        pdf_buffer = BytesIO()
        pdf = canvas.Canvas(pdf_buffer, pagesize=A4)
        width, height = A4
        y = height - 50

        pdf.setFont("Helvetica-Bold", 14)
        pdf.drawString(50, y, "Relatório de Simulação - Convexa")

        y -= 40
        pdf.setFont("Helvetica", 12)
        pdf.drawString(50, y, f"Aporte Inicial: {formata_reais(aporte_inicial)}")
        y -= 20
        pdf.drawString(50, y, f"Aporte Mensal: {formata_reais(aporte_mensal)}")
        y -= 20
        pdf.drawString(50, y, f"Total Investido: {formata_reais(total_aportes)}")
        y -= 20
        pdf.drawString(50, y, f"Rendimento Total: {formata_reais(rendimento_total)}")
        y -= 20
        pdf.drawString(50, y, f"Patrimônio Final: {formata_reais(patrimonio_final)}")

        if meta_valor > 0:
            y -= 20
            pdf.drawString(50, y, f"Meta: {formata_reais(meta_valor)}")
            if meses_atingido is not None and meses_atingido <= meses_acumulo:
                texto_meta_pdf = f"A meta será atingida em {anos_cheios} anos"
                if meses_restantes > 0:
                    texto_meta_pdf += f" e {meses_restantes} meses"
                y -= 20
                pdf.drawString(50, y, texto_meta_pdf)
            else:
                y -= 20
                pdf.drawString(50, y, "Meta não será atingida no período simulado.")

        # Inserir gráficos
        y -= 260
        pdf.drawImage(ImageReader(buffer_linha), 50, y, width=500, preserveAspectRatio=True)
        y -= 280
        pdf.drawImage(ImageReader(buffer_barra), 50, y, width=500, preserveAspectRatio=True)

        pdf.save()
        pdf_buffer.seek(0)

        b64 = base64.b64encode(pdf_buffer.read()).decode()
        href = f'<a href="data:application/pdf;base64,{b64}" download="relatorio_simulacao.pdf">📥 Clique aqui para baixar o PDF</a>'
        st.markdown(href, unsafe_allow_html=True)
