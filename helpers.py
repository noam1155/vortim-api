"""
helpers.py — כל פונקציות העזר של הפרויקט נמצאות כאן בלבד.
app.py מייבא מכאן. אל תכתוב לוגיקה כבדה בתוך ה-routes עצמם.

הפונקציות שתבנה כאן לפי ההנחיות (השמות מופיעים במסמכי docs/):
  load_vortim_for_parsha(parsha_name)
  load_single_vort(parsha_name, vort_id)
  is_long(text)
  load_users() / save_users(users)
  load_admins()
  hash_password(password) / verify_password(password, hashed)
  create_token(username) / decode_token(token)
  get_current_parsha()
  validate_vort(data)
"""

import json
from pathlib import Path
import config
from pyluach import dates, parshios
import bcrypt
import jwt
import datetime


BASE_DIR = Path(__file__).parent

PARSHIOT_DIR = BASE_DIR / 'data' / 'parshiot'


def is_long(text):
    lines_count = text.count('\n') + 1
    return lines_count > 20


def load_vortim_for_parsha(parsha_name):
    parsha_path = PARSHIOT_DIR / parsha_name

    if not parsha_path.exists():
        return None

    vortim = []

    for item in parsha_path.iterdir():
        if item.is_file() and item.name.endswith('.json'):
            with open(item, 'r', encoding='utf-8') as f:
                vort_data = json.load(f)
                vort_data['is_long'] = is_long(vort_data.get('text', ''))
                vortim.append(vort_data)

    return vortim


def load_single_vort(parsha_name, vort_id):
    filepath = PARSHIOT_DIR / parsha_name / f"{vort_id}.json"

    if not filepath.exists():
        return None

    with open(filepath, 'r', encoding='utf-8') as f:
        vort_data = json.load(f)
        vort_data['is_long'] = is_long(vort_data.get('text', ''))
        return vort_data


PARSHA_MAPPING = {
    "Bereshit": "bereshit",
    "Noach": "noach",
    "Lech Lecha": "lech_lecha"
}


def get_current_parsha():
    today = dates.HebrewDate.today()

    luach_parsha = parshios.getparsha_string(today, israel=True)


    if luach_parsha is None:
        return "bereshit"

    folder_name = PARSHA_MAPPING.get(luach_parsha, "bereshit")

    return folder_name


USERS_FILE = BASE_DIR / 'data' / 'users.json'

def load_users():
    """טוענת את המשתמשים מתוך הקובץ. אם אין קובץ, מחזירה מילון ריק."""
    if not USERS_FILE.exists():
        return {}
    with open(USERS_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_users(users):
    """שומרת את המילון של המשתמשים חזרה לקובץ."""
    with open(USERS_FILE, 'w', encoding='utf-8') as f:
        json.dump(users, f, indent=4)

def hash_password(password):
    """מצפינה את הסיסמה עם bcrypt"""
    bytes_password = password.encode('utf-8')
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(bytes_password, salt)
    return hashed.decode('utf-8')

def verify_password(password, hashed):
    """מאמתת את הסיסמה מול ה-hash"""
    bytes_password = password.encode('utf-8')
    bytes_hashed = hashed.encode('utf-8')
    return bcrypt.checkpw(bytes_password, bytes_hashed)

def create_token(username):
    """יוצרת token שמכיל את שם המשתמש ותוקף"""
    expiration = datetime.datetime.utcnow() + datetime.timedelta(hours=1)
    payload = {
        "username": username,
        "exp": expiration
    }
    token = jwt.encode(payload, config.JWT_SECRET, algorithm="HS256")
    return token





