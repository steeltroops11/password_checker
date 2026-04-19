import random
import string

SUBS = {'a': '@', 'e': '3', 'i': '!', 'o': '0', 's': '$'}
SPECIALS = '!@#$%^&*'


def improve_password(password):
    """Harden a weak password with substitutions, caps, and a suffix."""
    improved = []
    for ch in password:
        if ch.lower() in SUBS and random.random() < 0.5:
            improved.append(SUBS[ch.lower()])
        elif ch.isalpha() and random.random() < 0.4:
            improved.append(ch.upper())
        else:
            improved.append(ch)

    suffix = random.choice(SPECIALS) + str(random.randint(10, 99))
    result = ''.join(improved) + suffix

    while len(result) < 12:
        result += random.choice(string.ascii_letters + string.digits)
    return result


def generate_strong():
    """Generate a random 14-char password meeting all strength criteria."""
    guaranteed = [
        random.choice(string.ascii_uppercase),
        random.choice(string.ascii_lowercase),
        random.choice(string.digits),
        random.choice(SPECIALS),
    ]
    pool = string.ascii_letters + string.digits + SPECIALS
    remaining = [random.choice(pool) for _ in range(10)]
    password = guaranteed + remaining
    random.shuffle(password)
    return ''.join(password)
