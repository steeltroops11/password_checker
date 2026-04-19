import re


def check_strength(password):
    """Evaluate password strength against 5 security criteria."""
    criteria = {
        'length': len(password) >= 8,
        'uppercase': bool(re.search(r'[A-Z]', password)),
        'lowercase': bool(re.search(r'[a-z]', password)),
        'digit': bool(re.search(r'\d', password)),
        'special': bool(re.search(r'[!@#$%^&*(),.?":{}|<>\-_=+\[\]\\;\'`~]', password)),
    }

    score = sum(criteria.values())
    if score <= 2:
        level = 'Weak'
    elif score <= 4:
        level = 'Medium'
    else:
        level = 'Strong'

    return {'score': score, 'level': level, 'criteria': criteria}
