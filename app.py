"""
app.py — נקודת הכניסה של השרת.
כאן מגדירים את אפליקציית Flask ואת כל ה-routes.
פונקציות העזר לא נכתבות כאן — הן נמצאות ב-helpers.py ומיובאות לכאן.

בנה את הקובץ הזה לפי ההנחיות במסמכי docs/, שלב אחר שלב.
"""

from flask import Flask, jsonify, request
from helpers import load_vortim_for_parsha, load_single_vort, get_current_parsha, load_users, save_users, hash_password, verify_password, create_token



app = Flask(__name__)


@app.route('/', methods=['GET'])
def home():
    return jsonify({"status": "server is running"})


@app.route('/parshiot', methods=['GET'])
def get_parshiot():
    return jsonify(["bereshit", "noach", "lech_lecha"])


@app.route('/parshiot/<parsha>/vortim', methods=['GET'])
def get_vortim_by_parsha(parsha):
    vortim = load_vortim_for_parsha(parsha)

    if vortim is None:
        return jsonify({"error": f"Parsha '{parsha}' not found"}), 404

    return jsonify(vortim)


@app.route('/parshiot/<parsha>/vortim/<vort_id>', methods=['GET'])
def get_single_vort(parsha, vort_id):
    vort_data = load_single_vort(parsha, vort_id)

    if vort_data is None:
        return jsonify({"error": f"Vort '{vort_id}' not found in parsha '{parsha}'"}), 404

    return jsonify(vort_data)


@app.route('/current', methods=['GET'])
def current_parsha():
    parsha = get_current_parsha()
    return jsonify({"current_parsha": parsha})


@app.route('/current/vortim', methods=['GET'])
def current_parsha_vortim():
    parsha = get_current_parsha()

    vortim = load_vortim_for_parsha(parsha)

    if vortim is None:
        return jsonify({"error": f"No vortim found for current parsha '{parsha}'"}), 404

    return jsonify(vortim)


@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    users = load_users()

    if username in users:
        return jsonify({"error": "User already exists"}), 400

    hashed_pass = hash_password(password)
    users[username] = {"password": hashed_pass}
    save_users(users)

    return jsonify({"message": "User registered successfully"}), 201


@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    users = load_users()

    if username not in users:
        return jsonify({"error": "Invalid credentials"}), 401

    saved_hash = users[username]['password']
    if not verify_password(password, saved_hash):
        return jsonify({"error": "Invalid credentials"}), 401  # סיסמה שגויה מחזירה 401

    token = create_token(username)
    return jsonify({"token": token}), 200

if __name__ == '__main__':
    app.run(debug=True, port=5001)


