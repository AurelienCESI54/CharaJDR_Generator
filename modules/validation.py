# Validations
def validation(data):
    required_fields = {
        'nom': 'The character must have a name.',
        'age': 'The character must have an age.',
        'race': 'The character must have a race.',
        'pv': 'The character must have hit points.',
        'pd': 'The character must have damage points.',
        'descP': 'The character must have a description.',
        'descH': 'The character must have a story and/or relationships.',
        'background_path': "The background must be provided.",
        'avatar_path': "The avatar must be provided."
    }
    error = check_required_fields(data, required_fields)
    if error: return error

    positive_fields = {
        'age': 'Age cannot be negative.',
        'pv': 'Hit points cannot be negative.',
        'pd': 'Damage points cannot be negative.'
    }
    error = check_positive_fields(data, positive_fields)
    if error: return error

    max_length_fields = {
        'nom': (30, 'The name must be less than 30 characters.'),
        'descP': (500, 'The description must be less than 500 characters.'),
        'descH': (500, 'The history must be less than 500 characters.')
    }
    error = check_max_length_fields(data, max_length_fields)
    if error: return error

    competences = data.get('competences', [])
    error = validate_competences(competences)
    if error: return error

    return None

# Check that all numeric fields are positive or zero
def check_positive_fields(data, positive_fields):
    for field, message in positive_fields.items():
        value = data.get(field, None)
        if value is not None and value != '' and value < 0:
            return message
    return None

# Check that all required fields are present
def check_required_fields(data, required_fields):
    for field, message in required_fields.items():
        value = data.get(field, '')
        if not value:
            return message
    return None

# Check that all fields do not exceed the maximum length
def check_max_length_fields(data, max_length_fields):
    for field, (max_length, message) in max_length_fields.items():
        value = data.get(field, '')
        if value and len(value) > max_length:
            return message
    return None

# Skills validation
def validate_competences(competences):
    if not isinstance(competences, list):
        return "Malformed skills."
    if len(competences) < 2:
        return "You must enter at least 2 skills."
    if len(competences) > 6:
        return "You cannot enter more than 6 skills."
    for c in competences:
        if not c.get('nom') or not c.get('desc'):
            return "Each skill must have a name and a description."
        if len(c['nom']) > 30:
            return "A skill name must be less than 30 characters."
        if len(c['desc']) > 200:
            return "A skill description must be less than 200 characters."
    return None
