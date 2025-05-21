# Modules
from io import BytesIO
import os
from modules.pdfimg import *
from modules.pdftxt import *
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.utils import simpleSplit

def add_competences(pdf, competences, x=50, y_start=700, line_height=16, max_width=500):
    if not competences:
        return y_start
    
    page_width, _ = A4
    title = "SKILLS"
    font_name = "Helvetica-Bold"
    font_size = 14
    text_width = pdf.stringWidth(title, font_name, font_size)
    x_centered = (page_width - text_width) / 2

    pdf.setFont(font_name, font_size)
    pdf.setFillColorRGB(0, 0, 0)
    pdf.drawString(x_centered, y_start, title)
    y = y_start - line_height * 2

    font_name_name = "Helvetica-Bold"
    font_name_desc = "Helvetica"
    font_size_name = 12
    font_size_desc = 11

    for c in competences:
        name = c.get('nom', '').strip()[:30]
        desc = c.get('desc', '').strip()[:200]

        if not name or not desc:
            continue

        pdf.setFont(font_name_name, font_size_name)
        pdf.drawString(x, y, f"--- {name}")
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

def add_icons(pdf, hp, dmg, hp_icon, dmg_icon, y=25, icon_size=25, spacing=40):
    font_name = "Helvetica-Bold"
    font_size = 13
    page_width, _ = A4

    pdf.setFont(font_name, font_size)
    hp_text = str(hp)
    dmg_text = str(dmg)
    hp_text_width = pdf.stringWidth(hp_text, font_name, font_size)
    dmg_text_width = pdf.stringWidth(dmg_text, font_name, font_size)

    hp_block_width = icon_size + 3 + hp_text_width
    dmg_block_width = icon_size + 3 + dmg_text_width

    total_width = hp_block_width + spacing + dmg_block_width

    x_start = (page_width - total_width) / 2

    if hp_icon and os.path.exists(hp_icon):
        pdf.drawImage(hp_icon, x_start, y - icon_size + 4, width=icon_size, height=icon_size, mask='auto')
    pdf.drawString(x_start + icon_size + 3, y, hp_text)

    x_dmg = x_start + hp_block_width + spacing
    if dmg_icon and os.path.exists(dmg_icon):
        pdf.drawImage(dmg_icon, x_dmg, y - icon_size + 4, width=icon_size, height=icon_size, mask='auto')
    pdf.drawString(x_dmg + icon_size + 3, y, dmg_text)

    return y - icon_size - 6


def generatePDF(name, infos, competences=None, avatar_path=None, bg_path=None):
    buffer = BytesIO()
    pdf = canvas.Canvas(buffer, pagesize=A4)
    pdf.setTitle("JDR_Character")

    add_background(pdf, bg_path)
    add_title(pdf, name)
    draw_text_background(pdf, 30, 50, 530, 730, radius=16)
    add_avatar(pdf, avatar_path)

    y = 760
    bottom_margin = 40
    line_height = 14

    for info in infos:
        page_width, page_height = A4
        max_width = page_width - 100 - 50

        # If it's the HP/DMG line with icons
        if isinstance(info, dict) and 'pv' in info and 'pd' in info and 'vie_icon' in info and 'degat_icon' in info:
            needed_height = 24  # estimated height for the line with icons
            if y - needed_height < bottom_margin:
                pdf.showPage()
                add_background(pdf, bg_path)
                add_title(pdf, name)
                add_avatar(pdf, avatar_path)
                y = 760
            y = add_icons(pdf, info['pv'], info['pd'], info['vie_icon'], info['degat_icon'], y=y)
            y -= 10
            continue

        lines = simpleSplit(str(info), "Helvetica", 12, max_width)
        needed_height = len(lines) * line_height

        if y - needed_height < bottom_margin:
            pdf.showPage()
            add_background(pdf, bg_path)
            add_title(pdf, name)
            add_avatar(pdf, avatar_path)
            y = 760

        y = add_text(pdf, info, y)

    if competences:
        y = add_competences(pdf, competences, x=50, y_start=y - 20)

    pdf.save()
    buffer.seek(0)
    return buffer
