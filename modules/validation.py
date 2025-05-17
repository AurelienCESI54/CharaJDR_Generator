# Validations
def validation(data):
    required_fields = {
        'nom': 'Le personnage doit avoir un nom.',
        'age': 'Le personnage doit être âgé.',
        'race': 'Le personnage doit avoir une race.',
        'pv': 'Le personnage doit avoir de la vie.',
        'pd': 'Le personnage doit faire des dégâts.',
        'descP': 'Le personnage doit avoir une description.',
        'descH': 'Le personnage doit avoir une histoire et/ou des relations.',
        'background_path': "L'arrière-plan doit être fourni.",
        'avatar_path': "L'avatar doit être fourni."
    }
    error = check_required_fields(data, required_fields)
    if error: return error

    positive_fields = {
        'age': 'L\'âge ne peut pas être négatif.',
        'pv': 'La vie ne peut pas être négative.',
        'pd': 'Les dégâts ne peuvent pas être négatifs.'
    }
    error = check_positive_fields(data, positive_fields)
    if error: return error

    max_length_fields = {
        'nom': (30, 'Le nom doit faire moins de 30 caractères.'),
        'descP': (500, 'La description doit faire moins de 500 caractères.'),
        'descH': (500, 'L\'historique doit faire moins de 500 caractères.')
    }
    error = check_max_length_fields(data, max_length_fields)
    if error: return error

    competences = data.get('competences', [])
    error = validate_competences(competences)
    if error: return error

    return None

# Vérifie si tous les champs numériques sont positifs ou nuls
def check_positive_fields(data, positive_fields):
    for field, message in positive_fields.items():
        value = data.get(field, None)
        if value is not None and value != '' and value < 0:
            return message
    return None

# Vérifie si tous les champs obligatoires sont présents
def check_required_fields(data, required_fields):
    for field, message in required_fields.items():
        value = data.get(field, '')
        if not value:
            return message
    return None

# Vérifie si tous les champs ne dépassent pas la longueur maximale
def check_max_length_fields(data, max_length_fields):
    for field, (max_length, message) in max_length_fields.items():
        value = data.get(field, '')
        if value and len(value) > max_length:
            return message
    return None

# Validation des compétences
def validate_competences(competences):
    if not isinstance(competences, list):
        return "Compétences mal formatées."
    if len(competences) < 2:
        return "Vous devez saisir au moins 2 compétences."
    if len(competences) > 6:
        return "Vous ne pouvez pas saisir plus de 6 compétences."
    for c in competences:
        if not c.get('nom') or not c.get('desc'):
            return "Chaque compétence doit avoir un nom et une description."
        if len(c['nom']) > 30:
            return "Le nom d'une compétence doit faire moins de 30 caractères."
        if len(c['desc']) > 200:
            return "La description d'une compétence doit faire moins de 200 caractères."
    return None
