import hashlib
from pathlib import Path

import requests

DATA_FILE = Path(__file__).resolve().parent.parent / 'data' / 'common_passwords.txt'


def check_local(password):
    """Return True if password exists in the local common-passwords list."""
    if not DATA_FILE.exists():
        return False
    with DATA_FILE.open('r', encoding='utf-8') as f:
        return password in {line.strip() for line in f}


def check_hibp(password):
    """Query HaveIBeenPwned with k-anonymity. Return breach count (0 = safe)."""
    sha1 = hashlib.sha1(password.encode('utf-8')).hexdigest().upper()
    prefix, suffix = sha1[:5], sha1[5:]

    try:
        resp = requests.get(
            f'https://api.pwnedpasswords.com/range/{prefix}',
            headers={'User-Agent': 'PasswordChecker-Python'},
            timeout=5,
        )
        resp.raise_for_status()
    except Exception:
        return -1

    for line in resp.text.splitlines():
        hash_suffix, count = line.split(':')
        if hash_suffix == suffix:
            return int(count)
    return 0
