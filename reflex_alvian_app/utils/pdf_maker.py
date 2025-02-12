from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from io import BytesIO


def generate_detailed_pdf(nombre, profesion, ingresos, fecha_nacimiento, empresa, perfil_comercial, producto, monto_solicitado, plazo, cuota, garantia, scoring, deuda_financiera, ratio_deuda_ingresos, puntaje, dictamen, comentarios):
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4)
    styles = getSampleStyleSheet()
    story = []

    # Title
    title_style = styles['Title']
    title_style.alignment = 1  # Center alignment
    story.append(Paragraph("Dictamen de Crédito", title_style))
    story.append(Spacer(1, 0.2 * inch))

    # Custom subtitle style
    subtitle_style = ParagraphStyle(name='Subtitle', parent=styles['Heading2'], fontName='Helvetica-Bold', textColor=colors.white, backColor=colors.darkblue)

    # Datos del solicitante
    story.append(Table([[Paragraph("<font color='white'>Datos del Solicitante:</font>", subtitle_style)]], style=[('BACKGROUND', (0, 0), (-1, -1), colors.darkblue)]))
    story.append(Spacer(1, 0.1 * inch))

    normal_style = styles['Normal']
    data = [
        [Paragraph(f"<b>Nombre:</b> {nombre}", normal_style), Paragraph(f"<b>Fecha de Nacimiento:</b> {fecha_nacimiento}", normal_style)],
        [Paragraph(f"<b>Profesión:</b> {profesion}", normal_style), Paragraph(f"<b>Empresa:</b> {empresa}", normal_style)],
        [Paragraph(f"<b>Ingresos:</b> Gs. {format(ingresos, ',').replace(',', '.')}", normal_style), Paragraph(f"<b>Perfil Comercial:</b> {perfil_comercial}", normal_style)]
    ]
    table = Table(data)
    table.setStyle(TableStyle([
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
    ]))
    story.append(table)
    story.append(Spacer(1, 0.2 * inch))

    # Datos de la Operación
    story.append(Table([[Paragraph("<font color='white'>Datos de la Operación:</font>", subtitle_style)]], style=[('BACKGROUND', (0, 0), (-1, -1), colors.darkblue)]))
    story.append(Spacer(1, 0.1 * inch))
    data_operacion = [
        [Paragraph(f"<b>Producto:</b> {producto}", normal_style)],
        [Paragraph(f"<b>Monto solicitado:</b> Gs. {format(monto_solicitado, ',').replace(',', '.')}", normal_style)],
        [Paragraph(f"<b>Plazo:</b> {plazo}", normal_style)],
        [Paragraph(f"<b>Cuota:</b> Gs. {format(cuota, ',').replace(',', '.')}", normal_style)],
        [Paragraph(f"<b>Garantía:</b> {garantia}", normal_style)]
    ]
    table_operacion = Table(data_operacion)
    table_operacion.setStyle(TableStyle([
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
    ]))
    story.append(table_operacion)
    story.append(Spacer(1, 0.2 * inch))

    # Informe financiero
    story.append(Table([[Paragraph("<font color='white'>Informe Financiero:</font>", subtitle_style)]], style=[('BACKGROUND', (0, 0), (-1, -1), colors.darkblue)]))
    story.append(Spacer(1, 0.1 * inch))
    data_financiero = [
        [Paragraph(f"<b>Scoring:</b> {scoring}", normal_style)],
        [Paragraph(f"<b>Deuda financiera:</b> Gs. {format(deuda_financiera, ',').replace(',', '.')}", normal_style)],
        [Paragraph(f"<b>Ratio deuda/ingresos:</b> {ratio_deuda_ingresos}", normal_style)]
    ]
    table_financiero = Table(data_financiero)
    table_financiero.setStyle(TableStyle([
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
    ]))
    story.append(table_financiero)
    story.append(Spacer(1, 0.2 * inch))

    # Calificación final
    story.append(Table([[Paragraph("<font color='white'>Calificación Final:</font>", subtitle_style)]], style=[('BACKGROUND', (0, 0), (-1, -1), colors.darkblue)]))
    story.append(Spacer(1, 0.1 * inch))
    data_calificacion = [
        [Paragraph(f"<b>Puntaje:</b> {puntaje}", normal_style)],
        [Paragraph(f"<b>Dictamen:</b> {dictamen}", normal_style)]
    ]
    table_calificacion = Table(data_calificacion)
    table_calificacion.setStyle(TableStyle([
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
    ]))
    story.append(table_calificacion)
    story.append(Spacer(1, 0.2 * inch))

    # Comentarios
    story.append(Table([[Paragraph("<font color='white'>Comentarios:</font>", subtitle_style)]], style=[('BACKGROUND', (0, 0), (-1, -1), colors.darkblue)]))
    story.append(Spacer(1, 0.1 * inch))
    story.append(Paragraph(comentarios, normal_style))

    doc.build(story)
    buffer.seek(0)
    return buffer


if __name__ == "__main__":
    # Example data
    nombre = "John Doe"
    profesion = "Engineer"
    ingresos = 15000000
    fecha_nacimiento = "01/01/1980"
    empresa = "ACME Inc."
    perfil_comercial = "Employee"
    producto = "Personal Loan"
    monto_solicitado = 1000000
    plazo = 12
    cuota = 100000
    garantia = "None"
    scoring = "A"
    deuda_financiera = 5000000
    ratio_deuda_ingresos = 0.3
    puntaje = 18
    dictamen = "Approved"
    comentarios = "Good credit history"

    # Generate PDF
    pdf_buffer = generate_detailed_pdf(
        nombre=nombre,
        profesion=profesion,
        ingresos=ingresos,
        fecha_nacimiento=fecha_nacimiento,
        empresa=empresa,
        perfil_comercial=perfil_comercial,
        producto=producto,
        monto_solicitado=monto_solicitado,
        plazo=plazo,
        cuota=cuota,
        garantia=garantia,
        scoring=scoring,
        deuda_financiera=deuda_financiera,
        ratio_deuda_ingresos=ratio_deuda_ingresos,
        puntaje=puntaje,
        dictamen=dictamen,
        comentarios=comentarios
    )

    # Save PDF to file
    with open("financial_report.pdf", "wb") as f:
        f.write(pdf_buffer.getvalue())

    print("PDF generated successfully!")
