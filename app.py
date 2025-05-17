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

# Dossier d'upload pour les images
app.config['UPLOAD_FOLDER'] = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'upload_files')
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

@app.route('/', methods=['GET', 'POST'])
def index():
    data = {'nom': '',  'age': '',  'sexe': '',  'race': '',  'pv': '',  'pd': '',  'descP': '',  'descH': '', 'competences': '[]', 'background_filename': '', 'avatar_filename': ''}

    if request.method == 'POST':

        # Récupération des données
        fields = ['nom', 'age', 'sexe', 'race', 'pv', 'pd', 'descP', 'descH', 'competences']
        data.update(importForm(request.form, fields))
        data['background_filename'] = request.form.get('background_filename', '')
        data['avatar_filename'] = request.form.get('avatar_filename', '')

        # Conversion
        try:
            data['age'] = convert(data['age'], int)
            data['pv'] = convert(data['pv'], int)
            data['pd'] = convert(data['pd'], int)
        except ValueError:
            flash("Une valeur nombre est manquante ou incorrecte.", 'error')
            return restart(data)

        # Images
        background_file = request.files.get('background')
        if background_file and background_file.filename != '':
            ext = background_file.filename.rsplit('.', 1)[1].lower()
            bg_filename = f"bg_{data['nom']}_{data['age']}.{ext}"
            bg_path = handle_uploaded_image(
                background_file, ['jpg', 'jpeg', 'png'], app.config['UPLOAD_FOLDER'], bg_filename,
                "Format d'image non supporté pour l'arrière-plan.", render_template, data
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
            avatar_filename = f"avatar_{data['nom']}_{data['age']}.{ext}"
            avatar_path = handle_uploaded_image(
                avatar_file, ['jpg', 'jpeg', 'png'], app.config['UPLOAD_FOLDER'], avatar_filename,
                "Format d'image non supporté pour l'avatar.", render_template, data
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

        # Compétences
        competences = []
        if data.get('competences'):
            try:
                competences = json.loads(data['competences'])
                competences = [
                    {
                        'nom': c.get('nom', '').strip()[:30],
                        'desc': c.get('desc', '').strip()[:200]
                    }
                    for c in competences if c.get('nom') and c.get('desc')
                ]
            except Exception:
                flash("Erreur lors de la lecture des compétences.", 'error')
                return restart(data)
        data['competences'] = competences

        # Validations
        error = validation(data)
        if error:
            data['competences'] = json.dumps(data['competences'])
            flash(error, 'error')
            return restart(data)

        # PDF
        genre = data['sexe'] if data['sexe'] else "Asexué"
        infos = [
            f"{data['race']} de {data['age']} ans",
            f"Genre : {genre}",
            f"{data['pv']} points de vie - {data['pd']} points de dégâts",
            f"---",
            f"{data['descP'][:500]}",
            f"{data['descH'][:500]}"
        ]

        return send_file(
            generatePDF(
                data['nom'][:30],
                infos,
                competences=data['competences'],
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
