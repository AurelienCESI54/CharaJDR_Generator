# Modules
from io import BytesIO
from modules.pdfimg import *
from modules.pdftxt import *
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.utils import simpleSplit

def add_competences(pdf, competences, x=50, y_start=700, line_height=16, max_width=500):
    if not competences:
        return y_start
    
    page_width, _ = A4
    title = "COMPETENCES"
    font_name = "Helvetica-Bold"
    font_size = 14
    text_width = pdf.stringWidth(title, font_name, font_size)
    x_centered = (page_width - text_width) / 2

    pdf.setFont(font_name, font_size)
    pdf.setFillColorRGB(1, 1, 1)
    pdf.drawString(x_centered, y_start, title)
    y = y_start - line_height * 2

    font_name_nom = "Helvetica-Bold"
    font_name_desc = "Helvetica"
    font_size_nom = 12
    font_size_desc = 11

    for c in competences:
        nom = c.get('nom', '').strip()[:30]
        desc = c.get('desc', '').strip()[:200]

        if not nom or not desc:
            continue

        pdf.setFont(font_name_nom, font_size_nom)
        pdf.drawString(x, y, f"--- {nom}")
        y -= line_height

        pdf.setFont(font_name_desc, font_size_desc)
        lines = simpleSplit(desc, font_name_desc, font_size_desc, max_width)
        for line in lines:
            pdf.drawString(x + 10, y, line)
            y -= line_height

        y -= line_height // 2

        if y < 50:
            pdf.showPage()
            y = 750
            pdf.setFont(font_name, font_size)
            pdf.drawString(x_centered, y, title)
            y -= line_height * 2

    return y

def generatePDF(nom, infos, competences=None, avatar_path=None, bg_path=None):
    buffer = BytesIO()
    pdf = canvas.Canvas(buffer, pagesize=A4)
    pdf.setTitle("JDR_Character")

    add_background(pdf, bg_path)
    add_title(pdf, nom)
    draw_text_background(pdf, 30, 50, 530, 730, radius=16)
    add_avatar(pdf, avatar_path)

    y = 760
    bottom_margin = 40
    line_height = 14

    for info in infos:
        page_width, page_height = A4
        max_width = page_width - 100 - 50
        lines = simpleSplit(str(info), "Helvetica", 12, max_width)
        needed_height = len(lines) * line_height

        if y - needed_height < bottom_margin:
            pdf.showPage()
            add_background(pdf, bg_path)
            add_title(pdf, nom)
            add_avatar(pdf, avatar_path)
            y = 760

        y = add_text(pdf, info, y)

    if competences:
        y = add_competences(pdf, competences, x=50, y_start=y - 20)

    pdf.save()
    buffer.seek(0)
    return buffer
