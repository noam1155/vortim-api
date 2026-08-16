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








