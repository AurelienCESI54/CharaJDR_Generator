# Modules
import os
from flask import flash, render_template

# Data converter
def convert(data, format):
    try:
        return format(data)
    except (ValueError, TypeError):
        raise ValueError(f"Cannot convert '{data}' to {format.__name__}")

# Import data from form
def importForm(form, data):
    return {field: form.get(field, '').strip() for field in data}

# Reset form
def restart(data):
    return render_template('index.html', **data)

# Image handling
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
