# Modules
from io import BytesIO
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.utils import ImageReader
from reportlab.pdfbase.pdfmetrics import stringWidth
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import Paragraph
from reportlab.lib.enums import TA_JUSTIFY
from PIL import Image, ImageDraw

# Titre
def add_title(pdf, title):
    pdf.saveState()
    page_width = A4[0]
    font_name = "Helvetica-Bold"
    padding_x = 20
    box_side_padding = 2 * padding_x

    title, font_size, text_width = fit_title_font(title, font_name, page_width, padding=box_side_padding)

    box_width = text_width + box_side_padding
    box_height = font_size + 12
    x = (page_width - box_width) / 2
    y = 790

    draw_title_box(pdf, x, y, box_width, box_height)

    pdf.setFont(font_name, font_size)
    pdf.setFillColor(colors.blue)
    text_x = x + padding_x
    text_y = y + (box_height - font_size) / 2 + 2
    pdf.drawString(text_x, text_y, title)
    pdf.restoreState()

# Arrière-plan du titre
def draw_title_box(pdf, x, y, box_width, box_height):
    try:
        pdf.setFillAlpha(0.5)
    except AttributeError:
        pass
    pdf.setFillColor(colors.skyblue)
    pdf.setStrokeColor(colors.white)
    pdf.setLineWidth(2)
    pdf.roundRect(x, y, box_width, box_height, radius=12, fill=1, stroke=1)
    try:
        pdf.setFillAlpha(1)
    except AttributeError:
        pass

# Mise en forme du titre
def fit_title_font(title, font_name, max_width, min_font_size=8, padding=40):
    font_size = 16
    text_width = stringWidth(title, font_name, font_size)
    while text_width + padding > max_width and font_size > min_font_size:
        font_size -= 1
        text_width = stringWidth(title, font_name, font_size)
    if text_width + padding > max_width:
        # Tronque le texte si besoin
        while text_width + padding > max_width and len(title) > 3:
            title = title[:-4] + "..."
            text_width = stringWidth(title, font_name, font_size)
    return title, font_size, text_width

# Texte
def add_text(pdf, text, y, left_margin=50, right_margin=50):
    page_width, _ = A4
    max_width = page_width - left_margin - right_margin
    font_name = "Helvetica"
    font_size = 12

    styles = getSampleStyleSheet()
    justified_style = ParagraphStyle(
        'Justified',
        parent=styles['Normal'],
        fontName=font_name,
        fontSize=font_size,
        leading=font_size * 1.2,
        alignment=TA_JUSTIFY,
        textColor='white'
    )

    para = Paragraph(text, justified_style)

    w, h = para.wrap(max_width, y)
    para.drawOn(pdf, left_margin, y - h)

    return y - h - 10

# Arrière-plan du texte
def draw_text_background(pdf, x, y, width, height, radius=16):
    img = Image.new("RGBA", (int(width), int(height)), (0, 0, 0, int(0.6 * 255)))
    draw = ImageDraw.Draw(img)
    draw.rectangle([0, 0, width, height], outline=(255, 255, 255, 255), width=2)
    buffer = BytesIO()
    img.save(buffer, format="PNG")
    buffer.seek(0)
    pdf.drawImage(ImageReader(buffer), x, y, width=width, height=height, mask='auto')
