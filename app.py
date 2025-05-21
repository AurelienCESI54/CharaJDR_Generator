# Modules
from flask import Flask, request, flash, send_file, render_template
from modules.pdfgen import generatePDF
from modules.fonctions import *
import os
import json
from modules.validation import *

# Assets
app = Flask(__name__)
app.secret_key = 'charajdrgen'

# Upload folder for images
app.config['UPLOAD_FOLDER'] = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'upload_files')
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

@app.route('/', methods=['GET', 'POST'])
def index():
    data = {
        'name': '', 'age': '', 'gender': '', 'race': '', 'hp': '', 'dmg': '',
        'descP': '', 'descH': '', 'skills': '[]', 'background_filename': '', 'avatar_filename': ''
    }

    if request.method == 'POST':

        # Retrieve data
        fields = ['name', 'age', 'gender', 'race', 'hp', 'dmg', 'descP', 'descH', 'skills']
        data.update(importForm(request.form, fields))
        data['background_filename'] = request.form.get('background_filename', '')
        data['avatar_filename'] = request.form.get('avatar_filename', '')

        # Conversion
        try:
            data['age'] = convert(data['age'], int)
            data['hp'] = convert(data['hp'], int)
            data['dmg'] = convert(data['dmg'], int)
        except ValueError:
            flash("A numeric value is missing or incorrect.", 'error')
            return restart(data)

        # Images
        background_file = request.files.get('background')
        if background_file and background_file.filename != '':
            ext = background_file.filename.rsplit('.', 1)[1].lower()
            bg_filename = f"bg_{data['name']}_{data['age']}.{ext}"
            bg_path = handle_uploaded_image(
                background_file, ['jpg', 'jpeg', 'png'], app.config['UPLOAD_FOLDER'], bg_filename,
                "Unsupported image format for background.", render_template, data
            )
            if not (isinstance(bg_path, str) or bg_path is None):
                return bg_path
            data['background_filename'] = bg_filename
        elif data['background_filename']:
            bg_path = os.path.join(app.config['UPLOAD_FOLDER'], data['background_filename'])
        else:
            bg_path = None

        avatar_file = request.files.get('avatar')
        if avatar_file and avatar_file.filename != '':
            ext = avatar_file.filename.rsplit('.', 1)[1].lower()
            avatar_filename = f"avatar_{data['name']}_{data['age']}.{ext}"
            avatar_path = handle_uploaded_image(
                avatar_file, ['jpg', 'jpeg', 'png'], app.config['UPLOAD_FOLDER'], avatar_filename,
                "Unsupported image format for avatar.", render_template, data
            )
            if not (isinstance(avatar_path, str) or avatar_path is None):
                return avatar_path
            data['avatar_filename'] = avatar_filename
        elif data['avatar_filename']:
            avatar_path = os.path.join(app.config['UPLOAD_FOLDER'], data['avatar_filename'])
        else:
            avatar_path = None

        data['background_path'] = bg_path
        data['avatar_path'] = avatar_path

        # Skills
        skills = []
        if data.get('skills'):
            try:
                skills = json.loads(data['skills'])
                skills = [
                    {
                        'name': c.get('name', '').strip()[:30],
                        'desc': c.get('desc', '').strip()[:200]
                    }
                    for c in skills if c.get('name') and c.get('desc')
                ]
            except Exception:
                flash("Error reading skills.", 'error')
                return restart(data)
        data['skills'] = skills

        # Validations
        error = validation(data)
        if error:
            data['skills'] = json.dumps(data['skills'])
            flash(error, 'error')
            return restart(data)

        # PDF
        gender = data['gender'] if data['gender'] else "Agender"
        # Icon paths (adapt according to where you place them)
        hp_icon = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static', 'hp.png')
        dmg_icon = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static', 'dmg.png')
        infos = [
            f"{data['race']} aged {data['age']}",
            f"Gender: {gender}",
            {
                "hp": data['hp'],
                "dmg": data['dmg'],
                "hp_icon": hp_icon,
                "dmg_icon": dmg_icon
            },
            "---",
            f"{data['descP'][:500]}",
            f"{data['descH'][:500]}"
        ]

        return send_file(
            generatePDF(
                data['name'][:30],
                infos,
                competences=data['skills'],
                avatar_path=avatar_path,
                bg_path=bg_path
            ),
            as_attachment=True,
            download_name="JDR_Character.pdf",
            mimetype='application/pdf'
        )

    return render_template('index.html', **data)

if __name__ == '__main__':
    app.run(debug=True)
