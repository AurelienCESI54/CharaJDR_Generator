# Modules
import os
from flask import flash, render_template

# Convertisseur de données
def convert(data, format):
    try:
        return format(data)
    except (ValueError, TypeError):
        raise ValueError(f"Impossible de convertir '{data}' en {format.__name__}")

# Importation de données depuis le formulaire
def importForm(form, data):
    return {field: form.get(field, '').strip() for field in data}

# Restart du formulaire
def restart(data):
    return render_template('index.html', **data)

# Gestion d'image
def handle_uploaded_image(file, allowed_exts, upload_folder, filename, flash_msg, render_func, render_kwargs):
    if file and file.filename != '':
        ext = file.filename.rsplit('.', 1)[1].lower()
        if ext in allowed_exts:
            file_path = os.path.join(upload_folder, filename)
            file.save(file_path)
            return file_path
        else:
            flash(flash_msg, "error")
            return render_func('index.html', **render_kwargs)
    return None
