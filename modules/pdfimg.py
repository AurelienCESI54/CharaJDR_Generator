# Modules
from io import BytesIO
from reportlab.lib.pagesizes import A4
from reportlab.lib.utils import ImageReader
from PIL import Image, ImageDraw

# Arrière-plan
def add_background(pdf, bg_path):
    if bg_path:
        try:
            pdf.drawImage(
                ImageReader(bg_path),
                0, 0,
                width=A4[0],
                height=A4[1],
                preserveAspectRatio=False,
                mask='auto'
            )
        except Exception as e:
            print(f"Erreur lors de l'ajout de l'image de fond : {e}")

# Avatar
def add_avatar(pdf, avatar_path, x=500, y=750, size=75, border=4):
    if avatar_path:
        try:
            im = Image.open(avatar_path).convert("RGBA")
            im = im.resize((size, size), Image.LANCZOS)

            avatar_with_border = Image.new("RGBA", (size + 2*border, size + 2*border), (0, 0, 0, 0))
            draw = ImageDraw.Draw(avatar_with_border)
            draw.ellipse((0, 0, size + 2*border - 1, size + 2*border - 1), fill=(255, 255, 255, 255))

            mask = Image.new("L", (size, size), 0)
            mask_draw = ImageDraw.Draw(mask)
            mask_draw.ellipse((0, 0, size - 1, size - 1), fill=255)

            im.putalpha(mask)

            avatar_with_border.paste(im, (border, border), im)

            avatar_buffer = BytesIO()
            avatar_with_border.save(avatar_buffer, format="PNG")
            avatar_buffer.seek(0)

            pdf.drawImage(
                ImageReader(avatar_buffer),
                x - border, y - border,
                width=size + 2*border,
                height=size + 2*border,
                mask='auto'
            )
        except Exception as e:
            print(f"Erreur lors de l'ajout de l'avatar : {e}")
